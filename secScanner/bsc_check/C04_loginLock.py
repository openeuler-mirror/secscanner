import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")
from secScanner.commands.check_outprint import *

def rhel67_check_deny():
    InsertSection("check User login lock deny times and unlock time")
    regex = r'(?<=deny=).[0-9]*'
    DENY = ''
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('deny', line) and (not re.match('#', line)):
                temp = re.findall(regex, line)
                if temp != []:
                    DENY = temp[0]

    if DENY == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_02: %s", WRN_C04_02)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- No user login lock Deny set...", "WARNING")
    elif DENY > '5':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_01: %s", WRN_C04_01)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- Wrong user login lock Deny set...", "WARNING")
    else:
        logger.info("Has user login lock Deny set, checking OK")
        Display("- Has user login lock Deny set...", "OK")

def oe_rhel8_check_deny():
    InsertSection("check User login lock deny times and unlock time")
    regex = r'(?<=deny=).[0-9]*'
    DENY1 = ''
    DENY2 = ''
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('required', line) and re.search('pam_faillock.so', line) and (not re.match('#', line)):
                temp = re.findall(regex, line)
                if temp != []:
                    DENY1 = temp[0]
    with open("/etc/pam.d/password-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('required', line) and re.search('pam_faillock.so', line) and (not re.match('#', line)):
                temp = re.findall(regex, line)
                if temp != []:
                    DENY2 = temp[0]

    if DENY1 == '' and DENY2 == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_02: %s", WRN_C04_02)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- No user login lock Deny set...", "WARNING")
    elif DENY1 <= '5' or DENY2 <= '5':
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
    if OS_ID.lower() in ["centos", "rhel", "redhat", "openeuler", "bclinux"]:
        if OS_DISTRO in ["7", "6"]:
            rhel67_check_deny()
        elif OS_DISTRO in ["21.10", "20.12", "8"]:
            oe_rhel8_check_deny()
        else:
            InsertSection("check User login lock deny times and unlock time")
            logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        InsertSection("check User login lock deny times and unlock time")
        logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
