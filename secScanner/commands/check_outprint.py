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
from secScanner.lib import *
from secScanner.gconfig import * 
from secScanner.scan_func import cleanup 

logger = logging.getLogger('secscanner')

PRIVILEGED = 0
PENTESTINGMODE = 0
PROFILE = ""
PIDFILE = ""
ISVIRTUALMACHINE = 0
def distro_detection():
    global OS_DISTRO
    global OS_ID
    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("ID="):
                    OS_ID = line.split("=")[1].strip().strip("\"'")
                elif line.startswith("VERSION_ID"):
                    OS_DISTRO = line.split("=")[1].strip().strip("\"'").split('.')[0] # like VERSION_ID = "7"
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
                elif "CentOS" in line:
                    OS_ID = "centos"
                elif "Red" in line:
                    OS_ID = "rhel"
                elif any(cloud in line.lower() for cloud in ["bigcloud", "big"]):
                    OS_ID = "bclinux"
        if OS_ID and OS_DISTRO:
            logger.info(f"Detected this system is {OS_ID}-{OS_DISTRO}")
            Display(f"- Get the OS-ID:{OS_ID} and OS-version:{OS_DISTRO}...", "OK")
        else:
            logger.warning("Can't detect the OS_ID and OS_DISTRO from /etc/redhat-release file")
            Display("- Can't detect system type by /etc/redhat-release...", "WARNING")
    else:
        logger.warning("No os-release and redhat-release file, can not detect the OS_ID and OS_DISTRO")
        Display("- No os-release and redhat-release file...", "WARNING")
def check_myid():
    global MYID
    MYID = ""
    # Check user to determine file permissions later on. If we encounter Solaris, use related id binary instead
    try:
        MYID = subprocess.check_output(["/usr/xpg4/bin/id", "-u"]).decode().strip()
    except FileNotFoundError:
        MYID = subprocess.check_output(["id", "-u"]).decode().strip()

    if not MYID:
        print(f"Could not find user ID with id command. Want to help improving {PROGRAM_NAME}? Raise a ticket at {PROGRAM_SOURCE}")
        ExitFatal()

def check_param():
    global PRIVILEGED    
    global PENTESTINGMODE
    global LOGFILE
    if MYID == "0":
        PRIVILEGED = 1
    else:
        print(f"Start {PROGRAM_NAME} non-privileged")
        print("\n")
        PENTESTINGMODE = 1
    if PRIVILEGED == 0:
        if LOGFILE == "":
            LOGFILE = "/dev/null"

def find_profile():
    global PROFILE
    if PROFILE == "":
        tPROFILE_TARGETS = [
            "./secscanner.cfg",
            "/opt/secScanner/secscanner.cfg",
            "/etc/secScanner/secscanner.cfg"
        ]
        for I in tPROFILE_TARGETS:
            if os.path.isfile(I):
                PROFILE = I
                break

    if PROFILE == "":
        print(f"Fatal error: No profile defined and could not find default profile")
        print(f"Search paths used --> {tPROFILE_TARGETS}")
        ExitCustom(66)

def check_pid():
    global PIDFILE
    MYHOMEDIR = os.path.expanduser("~") or "/tmp"

    if PRIVILEGED == 0:
        PIDFILE = os.path.join(MYHOMEDIR, "secscanner.pid")
    elif os.path.isdir("/var/run"):
        PIDFILE = "/var/run/secscanner.pid"
    else:
        PIDFILE = "./secscanner.pid"

    # Check if there is already a PID file in any of the locations (incorrect termination of previous instance)
    if os.path.exists(os.path.join(MYHOMEDIR, "secscanner.pid")) or os.path.exists("./secscanner.pid") or os.path.exists("/var/run/secscanner.pid"):
        print("")
        print("      Warning: PID file exists, probably another secscanner process is running.")
        print("      ------------------------------------------------------------------------------")
        print("      If you are unsure another secscanner process is running currently, you are advised ")
        print("      to stop current process and check the process list first. If you cancelled")
        print("      (by using CTRL+C) a previous instance, you can ignore this message.")
        print("      ")
        print("      You are advised to check for temporary files after program completion.")
        print("      ------------------------------------------------------------------------------")
        print("")
        print("      Note: Cancelling the program can leave temporary files behind")
        print("")

        wait_for_keypress()

        # Deleting any stale PID files that might exist. Note: Display function does not work yet at this point
        if os.path.exists(os.path.join(MYHOMEDIR, "secscanner.pid")):
            os.remove(os.path.join(MYHOMEDIR, "secscanner.pid"))
        if os.path.exists("./secscanner.pid"):
            os.remove("./secscanner.pid")
        if os.path.exists("/var/run/secscanner.pid"):
            os.remove("/var/run/secscanner.pid")

    # Ensure symlink attack is not possible, by confirming there is no symlink of the file already
    OURPID = os.getpid()
    if os.path.islink(PIDFILE):
        print(f"Found symlinked PID file ({PIDFILE}), quitting")
        ExitFatal()
    else:
        # Create new PID file writable only by owner
        with open(PIDFILE, "w") as f:
            f.write(str(OURPID))
        os.chmod(PIDFILE, 0o600)


def display_info():

    InsertSection("Initializing program")

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lib_dir = os.path.join(current_dir, 'lib')

    osdetec_path = os.path.join(lib_dir, 'osdetection.py')
    try:
        subprocess.run(['python3', osdetec_path], check=True)
        Display("- Detecting OS...", "DONE")
    except subprocess.CalledProcessError as e:
        print(f"Error: osdetection - {e}")

    if subprocess.call('test -f /etc/os-release', shell=True) == 0:
        try:
            output = subprocess.check_output('cat /etc/os-release | grep -Eiw \'^PRETTY_NAME\'', shell=True)
            pretty_name = output.decode('utf-8').split('"')[1]
            OS_VERSION = pretty_name
        except Exception as e:
            return None

    OS = platform.system()
    distro_detection()
    OS_KERNELVERSION = platform.uname().release
    HARDWARE = platform.machine()
    HOSTNAME = platform.node()
    PROFILE = "/etc/secScanner/secscanner.cfg"
    python_version = platform.python_version()

    print("")
    print(f"  ---------------------------------------------------")
    print(f"  Program version:            {PROGRAM_version}")
    print(f"  Operating system:           {OS}")
    print(f"  Operating system name:      {OS_NAME}")
    print(f"  Operating system version:   {OS_VERSION}")
    print(f"  Kernel version:             {OS_KERNELVERSION}")
    print(f"  Hardware platform:          {HARDWARE}")
    print(f"  Hostname:                   {HOSTNAME}")
    print(f"  Profile:                    {PROFILE}")
    print(f"  Log file:                   {LOGFILE}")
    print(f"  Python version:             {python_version}")
    print("")
    print("  ---------------------------------------------------")

    logger.info(f"Program version:           {PROGRAM_version}")
    logger.info(f"Operating system:          {OS}")
    logger.info(f"Operating system name:     {OS_NAME}")
    logger.info(f"Operating system version:  {OS_VERSION}")
    logger.info(f"Kernel version:            {OS_KERNELVERSION}")
    logger.info(f"Hardware platform:         {HARDWARE}")
    logger.info("-----------------------------------------------------")
    logger.info(f"Hostname:                  {HOSTNAME}")
    logger.info(f"Profile:                   {PROFILE}")
    logger.info(f"Python version:            {python_version}")
    logger.info("-----------------------------------------------------")
    logger.info(f"Log file:                  {LOGFILE}")
    logger.info("===---------------------------------------------------------------===")

def check_isvirtualmachine():
    global ISVIRTUALMACHINE
    ISVIRTUALMACHINE, VMTYPE, VMFULLTYPE = IsVirtualMachine()
    if ISVIRTUALMACHINE == 1:
       Display(f"- Found virtual machine (type: {VMTYPE}, {VMFULLTYPE}) ", "DONE")
    elif ISVIRTUALMACHINE == 2:
        Display("- Unknown if this system is a virtual machine  ", "WARNING")
    else:
        Display("- System seems to be non-virtual  ", "DONE")

def end_parase():
    logger.info(f"{PROGRAM_name} {PROGRAM_version}")
    logger.info(f"{PROGRAM_copyright}")
    logger.info("Program ended successfully")
    logger.info("================================================================================")
    cleanup()

    if TOTAL_WARNINGS > 0:
        ExitCustom(78)
    else:
        ExitClean()

