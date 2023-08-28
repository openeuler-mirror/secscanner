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
from secScanner import gconfig

logger = logging.getLogger('secscanner')

def Display(text, result=''):
    color = ''
    if result == 'FINISHED' or result == "OK" or result == "DONE":
        color = gconfig.GREEN
    elif result == 'FAILED' or result == "WARNING":
        color = gconfig.RED
    elif result == 'SKIPPING' or 'SKIPPED':
        color = gconfig.YELLOW
    else:
        color = gconfig.NORMAL
    result_part = f"{color}{result}{gconfig.NORMAL}"
    print(text.ljust(60) + result)



def ExitClean():
    RemovePIDFile()
    RemoveTempFiles()
    PROGRAM_NAME = gconfig.PROGRAM_NAME
    logger.info(f"{gconfig.PROGRAM_NAME} ended successfully.")
    sys.exit(0)

def ExitCustom(exit_code=1):
    RemovePIDFile()
    RemoveTempFiles()
    if len(sys.argv) == 2:
        exit_code = int(sys.argv[1])

    PROGRAM_NAME = gconfig.PROGRAM_NAME
    
    logger.error(f"{gconfig.PROGRAM_NAME} ended with exit code {exit_code}.")
    sys.exit(exit_code)

def ExitFatal():
    RemovePIDFile()
    RemoveTempFiles()
    PROGRAM_NAME = gconfig.PROGRAM_NAME
    logger.error(f"{gconfig.PROGRAM_NAME} ended with exit code 1.")
    sys.exit(1)

def InsertSection(section_name):
    #if Const.QUIET == 0:
    print("")
    print(f"[+] {section_name} {gconfig.NORMAL}")
    print("------------------------------------")
    logger.info("===---------------------------------------------------------------===\n")
    logger.info(f"Action: Performing tests from category: {section_name}")


def IsVirtualMachine():
    logger.info("Test: Determine if this system is a virtual machine")
    #LogText("Test: Determine if this system is a virtual machine")
    ISVIRTUALMACHINE  = 2
    VMTYPE = VMTYPE = "unknown"
    VMFULLTYPE = VMFULLTYPE = "Unknown"
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

def loadtext(text):
    with open(TEXTINFOFILE, 'r') as file:
        for line in file:
            match = re.search(f'^.*Text="{re.escape(text)}".*', line)
            if match:
                return re.search('Text="(.*)"', match.group()).group(1)

def RemovePIDFile():
    # Test if PIDFILE is defined, before checking file presence
    if gconfig.PIDFILE:
        if os.path.isfile(gconfig.PIDFILE):
            os.remove(gconfig.PIDFILE)
            logger.info(f"PID file removed {gconfig.PIDFILE}")
        else:
            logger.error(f"PID file not found {gconfig.PIDFILE}")

def RemoveTempFiles():
    if gconfig.TEMP_FILES:
        logger.info(f"Temporary files: {gconfig.TEMP_FILES}")
        # Clean up temp files
        for FILE in gconfig.TEMP_FILES:
            # Temporary files should be in /tmp
            TMPFILE = re.match(r"^/tmp/secscanner", FILE)
            if TMPFILE:
                if os.path.isfile(TMPFILE):
                    logger.info(f"Action: removing temporary file {TMPFILE}")
                    os.remove(TMPFILE)
                else:
                    logger.warning(f"Info: temporary file {TMPFILE} was already removed")
            else:
                logger.info(f"Found invalid temporary file ({FILE}), not removed. Check your /tmp directory.")
    else:
        logger.info("No temporary files to be deleted")

def ReportException(id, text):
    logger.info(f"exception_event[]={id}|{text}|")
    logger.info(f"Exception: test has an exceptional event ({id}) with text {text}")

TOTAL_SUGGESTIONS = 0
TOTAL_WARNINGS = 0

def ReportSuggestion(test, message, details, solution):
    global TOTAL_SUGGESTIONS
    global TOTAL_WARNINGS
    TOTAL_SUGGESTIONS += 1
    if test == "":
        test = "UNKNOWN"
    if message == "":
        message = "UNKNOWN"
    if details == "":
        details = "-"
    if solution == "":
        solution = "-"
    logger.info(f"Suggestion: {message} [test:{test}] [details:{details}] [solution:{solution}]")

def ReportWarning(test, priority, text):
    global TOTAL_WARNINGS
    TOTAL_WARNINGS += 1

    if priority == "L" or priority == "M" or priority == "H":
        details = priority
        message = text
        solution = "-"
        logger.warning(f"warning[]={test}|{message}|{details}|{solution}|")
        logger.warning(f"Warning: {message} [test:{test}] [details:{details}] [solution:{solution}]")
    
    else:
        if test == "":
            test = "UNKNOWN"
        if text == "":
            message = "UNKNOWN"
        if priority == "":
            details = "-"
        if text == "":
            solution = "-"
        logger.warning(f"warning[]={test}|{message}|{details}|{solution}|")
        logger.warning(f"Warning: {message} [test:{test}] [details:{details}] [solution:{solution}]")

def IsRunning(process_name):
    RUNNING = 0
    PSOPTIONS = ""
    if SHELL_IS_BUSYBOX == 0:
        PSOPTIONS = "ax"
    FIND = subprocess.getoutput(f"{PSBINARY} {PSOPTIONS} | egrep '( |/){process_name}' | grep -v 'grep'")
    if FIND != "":
        RUNNING = 1
        logger.info(f"IsRunning: process '{process_name}' found ({FIND})")
    else:
        logger.info(f"IsRunning: process '{process_name}' not found")

    return RUNNING
"""
def Register(strINPUT):
    if SKIPLOGTEST == 0:
        logger.info("===---------------------------------------------------------------===\n")
    # 按空格分割输入字符串
    parts = strINPUT.split(' ')
    ROOT_ONLY = 0
    SKIPTEST = 0
    SKIPLOGTEST = 0
    TEST_NEED_OS = ""
    PREQS_MET = ""
    TEST_NEED_NETWORK = ""
    TEST_NEED_PLATFORM = ""
    TOTAL_TESTS = TOTAL_TESTS + 1

    # 遍历分割后的列表，提取值
    i = 0
    while i < len(parts):
        if parts[i] == '--platform':
            TEST_NEED_PLATFORM = parts[i+1]
        elif parts[i] == '--description':
            # 捕获完整的 --text 值
            description_parts = []
            while i + 1 < len(parts) and not parts[i+1].startswith('--'):
                description_parts.append(parts[i+1])
                i += 1
            TEST_DESCRIPTION = ' '.join(description_parts)
        elif parts[i] == '--network':
            TEST_NEED_NETWORK = parts[i+1]
        elif parts[i] == '--os':
            TEST_NEED_OS = parts[i+1]
        elif parts[i] == '--preqs-met':
            PREQS_MET = parts[i+1]
        elif parts[i] == '--root-only':
            if parts[i+1] == 'yes':
                ROOT_ONLY = 1
            elif parts[i+1] == 'no':
                ROOT_ONLY = 0
            else:
                logger.debug("Invalid option for --root-only parameter of Register function")
        elif parts[i] == '--test-no':
            TEST_NO = parts[i+1]
        elif parts[i] == '--weight':
            TEST_WEIGHT = parts[i+1]

        i += 1

    # Skip if a test is root only and we are running a non-privileged test
    if ROOT_ONLY == 1 and MYID != 0:
        SKIPTEST = 1
        SKIPREASON = "This test needs root permissions"
        SKIPPED_TESTS_ROOTONLY = f"{SKIPPED_TESTS_ROOTONLY}===={TEST_NO}:space:-:space:{TEST_DESCRIPTION}"

    # Skip test if it's configured in profile
    if SKIPTEST == 0:
        FIND = next((val for val in TEST_SKIP_ALWAYS if TEST_NO in val), None)
        if FIND:
            SKIPTEST = 1
            SKIPREASON = "Skipped by configuration"

    # Skip if test is not in the list
    if SKIPTEST == 0 and TESTS_TO_PERFORM:
        FIND = next((val for val in TESTS_TO_PERFORM if TEST_NO in val), None)
        if not FIND:
            SKIPTEST = 1
            SKIPREASON = "Test not in list of tests to perform"

    # Do not run scans which have a higher intensity than what we prefer
    if SKIPTEST == 0 and TEST_WEIGHT == "H" and SCAN_TEST_HEAVY == "NO":
        SKIPTEST = 1
        SKIPREASON = "Test too system intensive for scan mode (H)"
    if SKIPTEST == 0 and TEST_WEIGHT == "M" and SCAN_TEST_MEDIUM == "NO":
        SKIPTEST = 1
        SKIPREASON = "Test too system intensive for scan mode (M)"

    # Skip test if OS is different than requested
    if SKIPTEST == 0 and TEST_NEED_OS and OS != TEST_NEED_OS:
        SKIPTEST = 1
        SKIPREASON = "Incorrect guest OS ({TEST_NEED_OS} only)"
        if LOG_INCORRECT_OS == 0:
            SKIPLOGTEST = 1

    # Check for correct hardware platform
    if SKIPTEST == 0 and TEST_NEED_PLATFORM and HARDWARE != TEST_NEED_PLATFORM:
        SKIPTEST = 1
        SKIPREASON = "Incorrect hardware platform"

    # Not all prerequisites met, like missing tool
    if SKIPTEST == 0 and PREQS_MET == "NO":
        SKIPTEST = 1
        SKIPREASON = "Prerequisities not met (i.e. missing tool, other type of Linux distribution)"

    # Skip test?
    if SKIPTEST == 0:
        # First wait X seconds (depending pause_between_tests)
        if TEST_PAUSE_TIME > 0:
            time.sleep(TEST_PAUSE_TIME)

        # Increase counter for every registered test which is performed
        counttests()
        if SKIPLOGTEST == 0:
            logger.info(f"Performing test ID {TEST_NO} ({TEST_DESCRIPTION})")
            #LogText(f"Performing test ID {TEST_NO} ({TEST_DESCRIPTION})")
        TESTS_EXECUTED = f"{TEST_NO}|{TESTS_EXECUTED}"
    else:
        if SKIPLOGTEST == 0:
            logger.warning(f"Skipped test {TEST_NO} ({TEST_DESCRIPTION})")
            #LogText(f"Skipped test {TEST_NO} ({TEST_DESCRIPTION})")
        if SKIPLOGTEST == 0:
            logger.warning(f"Reason to skip: {SKIPREASON}")
            #LogText(f"Reason to skip: {SKIPREASON}")
        TESTS_SKIPPED = f"{TEST_NO}|{TESTS_SKIPPED}"
"""

def wait_for_keypress():
    try:
        getpass.getpass("\n[ Press [ENTER] to continue, or [CTRL]+C to stop ]")
    except KeyboardInterrupt:
        sys.exit()
