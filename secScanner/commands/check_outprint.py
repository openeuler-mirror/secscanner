# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''



import os
import sys
import subprocess
import logging
import pwd
import platform
import importlib.util
# from .basic import *
from secScanner.lib.function import *
#from secScanner.gconfig import * 
from secScanner.lib.errors import *
from datetime import datetime

logger = logging.getLogger('secscanner')

def distro_detection():
    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("ID="):
                    OS_ID = line.split("=")[1].strip().strip("\"'")
                    set_value("OS_ID", OS_ID)
                elif line.startswith("VERSION_ID"):
                    tmp_distro = line.split("=")[1].strip().strip("\"'")
                    if tmp_distro.startswith("7") or tmp_distro.startswith("8"):
                        OS_DISTRO = tmp_distro[0] # 7，8系列
                    elif tmp_distro.startswith("2"): # 欧拉系列
                        OS_DISTRO = tmp_distro
                    set_value("OS_DISTRO", OS_DISTRO)
                elif line.startswith("VERSION"):
                    SYS_VERSION = line.split("=")[1].strip().strip("\"'")
                    set_value("SYS_VERSION", SYS_VERSION)
        if OS_ID and OS_DISTRO:
            if OS_ID.lower() in ["centos", "rhel", "redhat", "openeuler", "bclinux"]:
                logger.info(f"Detected this system is {OS_ID}-{OS_DISTRO}")
                Display(f"- Get the OS-ID:{OS_ID} and OS-version:{OS_DISTRO}...", "OK")
            else:
                logger.warning(f"This is not centos/redhat/openEuler/bclinux Distro, we do not support {OS_ID}-{OS_DISTRO} at this moment, according to /etc/os-release")
                Display("- Can't detect system type by /etc/os-release...", "WARNING")
        else:
            logger.warning("Can't detect the OS_ID and OS_DISTRO from /etc/os-release file")
            Display("- Can't detect system type by /etc/os-release...", "WARNING")

    elif os.path.isfile("/etc/redhat-release"):
        with open("/etc/redhat-release") as f:
            for line in f:
                if any(version in line for version in ["6", "7"]):
                    OS_DISTRO = line.split(".")[0]
                    set_value("OS_DISTRO", OS_DISTRO)
                elif "CentOS" in line:
                    OS_ID = "centos"
                elif "Red" in line:
                    OS_ID = "rhel"
                elif any(cloud in line.lower() for cloud in ["bigcloud", "big"]):
                    OS_ID = "bclinux"
                set_value("OS_ID", OS_ID)
        if OS_ID and OS_DISTRO:
            logger.info(f"Detected this system is {OS_ID}-{OS_DISTRO}")
            Display(f"- Get the OS-ID:{OS_ID} and OS-version:{OS_DISTRO}...", "OK")
        else:
            logger.warning("Can't detect the OS_ID and OS_DISTRO from /etc/redhat-release file")
            Display("- Can't detect system type by /etc/redhat-release...", "WARNING")
    else:
        logger.warning("No os-release and redhat-release file, can not detect the OS_ID and OS_DISTRO")
        Display("- No os-release and redhat-release file...", "WARNING")

def find_profile():
    val_dict = show_dict()
    if "PROFILE" in val_dict:
        PROFILE = get_value("PROFILE")
    else:
        PROFILE = ""
    if PROFILE == "":
        PROFILE_TARGETS = [
            "./secscanner.cfg",
            "/opt/secScanner/secscanner.cfg",
            "/etc/secScanner/secscanner.cfg"
        ]
        for I in PROFILE_TARGETS:
            if os.path.isfile(I):
                PROFILE = I
                set_value("PROFILE", PROFILE)
                break

    if PROFILE == "":
        ConfigError('Fatal error: No profile defined and could not find default profile')

def display_info():

    InsertSection("Initializing program")
    report_datetime_start = datetime.now()
    report_datetime_start = set_value("report_datetime_start",report_datetime_start)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_dir = os.path.join(current_dir, 'lib')

    if subprocess.call('test -f /etc/os-release', shell=True) == 0:
        try:
            output = subprocess.check_output('cat /etc/os-release | grep -Eiw \'^PRETTY_NAME\'', shell=True)
            pretty_name = output.decode('utf-8').split('"')[1]
            OS_VERSION = pretty_name
            set_value("OS_VERSION", OS_VERSION)
        except Exception as e:
            return None

    OS = platform.system()
    distro_detection()
    OS_NAME = get_value("OS_NAME")
    OS_VERSION = get_value("OS_VERSION")
    OS_KERNELVERSION_FULL = platform.uname().release
    HARDWARE = platform.machine()
    HOSTNAME = platform.node()
    PROFILE = "/etc/secScanner/secscanner.cfg"
    PYTHON_VERSION = platform.python_version()
    HOSTNAME = set_value("HOSTNAME",HOSTNAME)
    OS_KERNELVERSION_FULL = set_value("OS_KERNELVERSION_FULL",OS_KERNELVERSION_FULL)
    print("")
    print(f"  ---------------------------------------------------")
    print(f"  Program version:            {PROGRAM_VERSION}")
    print(f"  Operating system:           {OS}")
    print(f"  Operating system name:      {OS_NAME}")
    print(f"  Operating system version:   {OS_VERSION}")
    print(f"  Kernel version:             {OS_KERNELVERSION_FULL}")
    print(f"  Hardware platform:          {HARDWARE}")
    print(f"  Hostname:                   {HOSTNAME}")
    print(f"  Profile:                    {PROFILE}")
    print(f"  Log file:                   {LOGFILE}")
    print(f"  Python version:             {PYTHON_VERSION}")
    print("")
    print("  ---------------------------------------------------")

    logger.info(f"Program version:           {PROGRAM_VERSION}")
    logger.info(f"Operating system:          {OS}")
    logger.info(f"Operating system name:     {OS_NAME}")
    logger.info(f"Operating system version:  {OS_VERSION}")
    logger.info(f"Kernel version:            {OS_KERNELVERSION_FULL}")
    logger.info(f"Hardware platform:         {HARDWARE}")
    logger.info("-----------------------------------------------------")
    logger.info(f"Hostname:                  {HOSTNAME}")
    logger.info(f"Profile:                   {PROFILE}")
    logger.info(f"Python version:            {PYTHON_VERSION}")
    logger.info("-----------------------------------------------------")
    logger.info(f"Log file:                  {LOGFILE}")
    logger.info("===---------------------------------------------------------------===")

def check_isvirtualmachine():
    ISVIRTUALMACHINE, VMTYPE, VMFULLTYPE = IsVirtualMachine()
    set_value("ISVIRTUALMACHINE", ISVIRTUALMACHINE)
    if ISVIRTUALMACHINE == 1:
       Display(f"- Found virtual machine (type: {VMTYPE}, {VMFULLTYPE}) ", "DONE")
    elif ISVIRTUALMACHINE == 2:
        Display("- Unknown if this system is a virtual machine  ", "WARNING")
    else:
        Display("- System seems to be non-virtual  ", "DONE")

def end_parase():
    logger.info(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
    logger.info(f"{PROGRAM_COPYRIGHT}")
    logger.info("Program ended successfully")
    logger.info("================================================================================")


