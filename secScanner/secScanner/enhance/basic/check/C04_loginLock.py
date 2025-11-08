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
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")
from secScanner.commands.check_outprint import *


def el67_check_deny():
    regex = r'(?<=deny=).[0-9]*'
    DENY = ''
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('deny', line) and (not re.match('#', line)):
                temp = re.findall(regex, line)
                if temp:
                    DENY = temp[0]

    if DENY == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_02: %s", WRN_C04_02)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- No user login lock Deny set...", "WARNING")
    elif int(DENY) > 5:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_01: %s", WRN_C04_01)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- Wrong user login lock Deny set...", "WARNING")
    else:
        logger.info("Has user login lock Deny set, checking OK")
        Display("- Has user login lock Deny set...", "OK")


def oe_el8_check_deny():
    regex = r'(?<=deny=).[0-9]*'
    regex2 = r'(?<=unlock_time=).[0-9]*'
    DENY1 = ''
    DENY2 = ''
    DENY3 = ''
    DENY4 = ''
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('required', line) and re.search('pam_faillock.so', line) and (
            not re.match('#', line)):
                temp = re.findall(regex, line)
                temp2 = re.findall(regex2, line)
                if temp:
                    DENY1 = temp[0]
                if temp2:
                    DENY3 = temp2[0]
    with open("/etc/pam.d/password-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('required', line) and re.search('pam_faillock.so', line) and (
            not re.match('#', line)):
                temp = re.findall(regex, line)
                temp2 = re.findall(regex2, line)
                if temp:
                    DENY2 = temp[0]
                if temp2:
                    DENY4 = temp2[0]

    if DENY1 == '' and DENY2 == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_02: %s", WRN_C04_02)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- No user login lock Deny set...", "WARNING")
    elif int(DENY1) <= 5 and int(DENY2) <= 5 and int(DENY3) >= 300 and int(DENY4) >= 300 :
        logger.info("Has user login lock Deny set, checking OK")
        Display("- Has user login lock Deny set...", "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_01: %s", WRN_C04_01)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- Wrong user login lock Deny set...", "WARNING")


def C04_loginLock():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("check User login lock deny times and unlock time")
    if OS_ID.lower() in ["centos", "rhel", "redhat", "openeuler", "bclinux"]:
        if OS_DISTRO in ["7", "6"]:
            el67_check_deny()
        elif OS_DISTRO in SUPPORT_VER:
            oe_el8_check_deny()
        else:
            logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
