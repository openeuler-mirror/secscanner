import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")
from secScanner.commands.check_outprint import *


def el7_check_deny():
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
    elif DENY > '5':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC04\n")
        logger.warning("WRN_C04_01: %s", WRN_C04_01)
        logger.warning("SUG_C04: %s", SUG_C04)
        Display("- Wrong user login lock Deny set...", "WARNING")
    else:
        logger.info("Has user login lock Deny set, checking OK")
        Display("- Has user login lock Deny set...", "OK")


def C01_loginLock():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("check User login lock deny times and unlock time")
    if OS_ID.lower() in ["centos", "rhel", "redhat", "openeuler", "bclinux"]:
        if OS_DISTRO in ["7", "6"]:
            el67_check_deny()
        elif OS_DISTRO in ["21.10", "20.12", "8", "22.10U1", "22.10", "22.10U2", "22.03", "v24", "24"]:
            oe_el8_check_deny()
        else:
            logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.warning(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
