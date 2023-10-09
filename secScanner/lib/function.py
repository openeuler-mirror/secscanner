# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, 
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, 
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''


import logging
import os
import sys
import re
import getpass
import subprocess
import configparser
from secScanner.gconfig import *

logger = logging.getLogger('secscanner')

def Display(text, result=''):
    color = ''
    if result == 'FINISHED' or result == "OK" or result == "DONE":
        color = GREEN
    elif result == 'FAILED' or result == "WARNING":
        color = RED
    elif result == 'SKIPPING' or 'SKIPPED':
        color = YELLOW
    else:
        color = NORMAL
    result_part = f"{color}{result}{NORMAL}"
    print(text.ljust(80) + '[ ' + result_part + ' ]')

def InsertSection(section_name):
    print("")
    print(f"[+] {section_name} {NORMAL}")
    print("------------------------------------")
    logger.info("===---------------------------------------------------------------===\n")
    logger.info(f"Action: Performing tests from category: {section_name}")

def IsVirtualMachine():
    logger.info("Test: Determine if this system is a virtual machine")
    #LogText("Test: Determine if this system is a virtual machine")
    ISVIRTUALMACHINE  = 2
    VMTYPE = "unknown"
    VMFULLTYPE = "Unknown"
    SHORT = ""

    # facter
    if SHORT == "":
        if subprocess.call(["which", "facter"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 :
            output = subprocess.check_output(["facter", "is_virtual"]).decode().strip()
            if output == "true":
                SHORT = subprocess.check_output(["facter", "virtual"]).decode().strip()
                logger.info(f"Result: found {SHORT}")
            elif output == "false":
                logger.info("Result: facter says this machine is not a virtual")
        else:
            logger.warning("Result: facter utility not found")
    else:
        logger.info("Result: skipped facter test, as we already found machine type")

    # systemd
    if SHORT == "":
        if subprocess.call(["which", "systemd-detect-virt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            logger.info("Test: trying to guess virtualization technology with systemd-detect-virt")
            FIND = subprocess.check_output(["systemd-detect-virt"]).decode().strip()
            if FIND != "":
                logger.info(f"Result: found {FIND}")
                SHORT = FIND
        else:
            logger.error("Result: systemd-detect-virt not found")
    else:
        logger.info("Result: skipped systemd test, as we already found machine type")

    # lscpu
    if SHORT == "":
        if subprocess.call(["which", "lscpu"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            logger.info("Test: trying to guess virtualization with lscpu")
            FIND = subprocess.check_output(["lscpu | grep '^Hypervisor Vendor' | awk -F: '{ print $2 }' | sed 's/ //g'"], shell=True).decode().strip()
            if FIND != "":
                logger.info(f"Result: found {FIND}")
                SHORT = FIND
            else:
                logger.warning("Result: can't find hypervisor vendor with lscpu")
        else:
            logger.error("Result: lscpu not found")
    else:
        logger.info("Result: skipped lscpu test, as we already found machine type")
    
    # dmidecode
    if SHORT == "":
        if subprocess.call(["which", "dmidecode"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            logger.info("Test: trying to guess virtualization with dmidecode")
            FIND = subprocess.check_output(["dmidecode -s system-product-name | awk '{ print $1 }'"], shell=True).decode().strip()
            if FIND != "":
                logger.info(f"Result: found {FIND}")
                SHORT = FIND
            else:
                logger.warning("Result: can't find product name with dmidecode")
        else:
            logger.error("Result: dmidecode not found")
    else:
        logger.info("Result: skipped dmidecode test, as we already found machine type")

    # lshw
    if SHORT == "":
        if subprocess.call(["which", "lshw"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            logger.info("Test: trying to guess virtualization with lshw")
            FIND = subprocess.check_output(["lshw -quiet -class system | awk '{ if ($1=='product:') { print $2 }}'"], shell=True).decode().strip()
            if FIND != "":
                logger.info(f"Result: found {FIND}")
                SHORT = FIND
        else:
            logger.error("Result: lshw not found")
    else:
        logger.info("Result: skipped lshw test, as we already found machine type")
   
   # Try common guest processes
    if SHORT == "":
        logger.info("Test: trying to guess virtual machine type by running processes")
        # VMware
        process_name = "vmware-guestd"
        RUNNING = IsRunning(process_name)
        if RUNNING == 1:
            SHORT = "vmware"

        process_name = "vmtoolsd"
        RUNNING = IsRunning(process_name)
        if RUNNING == 1:
            SHORT = "vmware"

        # VirtualBox based on guest services
        process_name = "vboxguest-service"
        RUNNING = IsRunning(process_name)
        if RUNNING == 1:
            SHORT = "virtualbox"

        process_name = "VBoxClient"
        RUNNING = IsRunning(process_name)
        if RUNNING == 1:
            SHORT = "virtualbox"
    else:
        logger.info("Result: skipped processes test, as we already found platform")

    # Amazon EC2
    if SHORT == "":
        logger.info("Test: checking specific files for Amazon")
        if os.path.isfile("/etc/ec2_version") and os.path.getsize("/etc/ec2_version") != 0:
            SHORT = "amazon-ec2"
        else:
            logger.info("Result: system not hosted on Amazon")
    else:
        logger.info("Result: skipped Amazon EC2 test, as we already found platform")

    # sysctl values
    if SHORT == "":
        logger.info("Test: trying to guess virtual machine type by sysctl keys")
        FIND = subprocess.check_output(["sysctl -a 2> /dev/null | egrep '(hw.product|machdep.dmi.system-product)' | head -1 | sed 's/ = /=/' | awk -F= '{ print $2 }'"], shell=True).decode().strip()
        if FIND != "":
            SHORT = FIND
    else:
        logger.info("Result: skipped sysctl test, as we already found platform")

    if not SHORT == "":
    # Lowercase and see if we found a match
        SHORT = SHORT.split(" ")[0].lower()

        if SHORT == "amazon-ec2":
            ISVIRTUALMACHINE = 1
            VMTYPE = "amazon-ec2"
            VMFULLTYPE = "Amazon AWS EC2 Instance"
        elif SHORT == "bochs":
            ISVIRTUALMACHINE = 1
            VMTYPE = "bochs"
            VMFULLTYPE = "Bochs CPU emulation"
        elif SHORT == "docker":
            ISVIRTUALMACHINE = 1
            VMTYPE = "docker"
            VMFULLTYPE = "Docker container"
        elif SHORT == "kvm":
            ISVIRTUALMACHINE = 1
            VMTYPE = "kvm"
            VMFULLTYPE = "KVM"
        elif SHORT == "lxc":
            ISVIRTUALMACHINE = 1
            VMTYPE = "lxc"
            VMFULLTYPE = "Linux Containers"
        elif SHORT == "lxc-libvirt":
            ISVIRTUALMACHINE = 1
            VMTYPE = "lxc-libvirt"
            VMFULLTYPE = "libvirt LXC driver (Linux Containers)"
        elif SHORT == "microsoft":
            ISVIRTUALMACHINE = 1
            VMTYPE = "microsoft"
            VMFULLTYPE = "Microsoft Virtual PC"
        elif SHORT == "openvz":
            ISVIRTUALMACHINE = 1
            VMTYPE = "openvz"
            VMFULLTYPE = "OpenVZ"
        elif SHORT in ["oracle", "virtualbox"]:
            ISVIRTUALMACHINE = 1
            VMTYPE = "virtualbox"
            VMFULLTYPE = "Oracle VM VirtualBox"
        elif SHORT == "qemu":
            ISVIRTUALMACHINE = 1
            VMTYPE = "qemu"
            VMFULLTYPE = "QEMU"
        elif SHORT == "systemd-nspawn":
            ISVIRTUALMACHINE = 1
            VMTYPE = "systemd-nspawn"
            VMFULLTYPE = "Systemd Namespace container"
        elif SHORT == "uml":
            ISVIRTUALMACHINE = 1
            VMTYPE = "uml"
            VMFULLTYPE = "User-Mode Linux (UML)"
        elif SHORT == "vmware":
            ISVIRTUALMACHINE = 1
            VMTYPE = "vmware"
            VMFULLTYPE = "VMware product"
        elif SHORT == "xen":
            ISVIRTUALMACHINE = 1
            VMTYPE = "xen"
            VMFULLTYPE = "XEN"
        elif SHORT == "zvm":
            ISVIRTUALMACHINE = 1
            VMTYPE = "zvm"
            VMFULLTYPE = "IBM z/VM"
        else:
            logger.info("Result: Unknown virtualization type, so most likely system is physical")

    if ISVIRTUALMACHINE == 1:
        logger.info(f"Result: found virtual machine (type: {VMTYPE}, {VMFULLTYPE})")
        logger.info("vm=1")
        logger.info(f"vmtype={VMTYPE}")
    elif ISVIRTUALMACHINE == 2:
        logger.info("Result: unknown if this system is a virtual machine")
        logger.info("vm=2")
    else:
        logger.info("Result: system seems to be non-virtual")

    return ISVIRTUALMACHINE, VMTYPE, VMFULLTYPE

def IsRunning(process_name):  # PSBINARY is not defined
    RUNNING = 0
    PSOPTIONS = ""
    PSBINARY = "ps"
    SHELL_IS_BUSYBOX = get_value("SHELL_IS_BUSYBOX")
    if SHELL_IS_BUSYBOX == "0":
        PSOPTIONS = "ax"
    FIND = subprocess.getoutput(f"{PSBINARY} {PSOPTIONS} | egrep '( |/){process_name}' | grep -v 'grep'")
    if FIND != "":
        RUNNING = 1
        logger.info(f"IsRunning: process '{process_name}' found ({FIND})")
    else:
        logger.info(f"IsRunning: process '{process_name}' not found")
    return RUNNING

def wait_for_keypress():
    try:
        getpass.getpass("\n[ Press [ENTER] to continue, or [CTRL]+C to stop ]")
    except KeyboardInterrupt:
        sys.exit()

def make_oval_definition(one_sample, field_list, write_file):
    if 'openeulercvrf' in one_sample.__tablename__.lower():
        definition_class = 'security advisory'
    else:
        definition_class = 'vulnerability'
    write_file.write(f"<definition id=\"oval:org.bclinux.security:def:{one_sample.id}\" version=\"1\" class=\"{definition_class}\">\n")
    write_file.write("<metadata>\n")
    for field in field_list:
        if field == '_sa_instance_state':
            continue
        write_file.write(f"<{field}>{one_sample.__dict__[field]}</{field}>\n")
    write_file.write("</metadata>\n")
    write_file.write("</definition>\n")

def make_one_json(one_sample, field_list, write_file):

    for i in range(len(field_list)):
        if field_list[i] == '_sa_instance_state':
            continue
        temp = one_sample.__dict__[field_list[i]]
        write_file.write(f"\"{field_list[i]}\": \"{temp}\"\n")
        if i != (len(field_list)-1):
            write_file.write(",\n")
def make_json_file(all_samples, table = CVRF):
    with open(f'{table.__tablename__}.json', 'w') as write_file:
        write_file.write("[\n")
        for j in range(len(all_samples)):
            field_list = list(all_samples[j].__dict__)
            write_file.write("{")
            make_one_json(all_samples[j], field_list, write_file)
            write_file.write("}")
            if j != len(all_samples)-1:
                write_file.write(",\n")
        write_file.write("]\n")


