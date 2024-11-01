import logging
import re
import os
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C35_nologinList():
    InsertSection("check list of users prohibited from login")
    check_flag_sys = False
    check_flag_paswd = False
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('pam_listfile.so', line):
                check_flag_sys = True

    with open('/etc/pam.d/password-auth', 'r') as read_file:
        lines = read_file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('pam_listfile.so', line):
                check_flag_paswd = True

    if not check_flag_sys and not check_flag_paswd:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC35\n")
        logger.warning("WRN_C35_01: %s", WRN_C35_01)
        logger.warning("SUG_C35: %s", SUG_C35)
        Display("- No list of users prohibited from login set...", "WARNING")
    elif not os.path.exists('/etc/login.user.deny'):
        with open(RESULT_FILE, "a") as file:
            file.write("\nC35\n")
        logger.warning("WRN_C35_02: %s", WRN_C35_02)
        logger.warning("SUG_C35: %s", SUG_C35)
        Display("- No path /etc/login.user.deny...", "WARNING")
    else:
        logger.info("Has list of users prohibited from login set, checking OK")
        Display("- Check the list of users prohibited from login...", "OK")
