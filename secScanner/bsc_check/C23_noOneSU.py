import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C23_noOneSU():
    InsertSection("check if permit user can su to root")
    # LINE_NUMBER = 0 # dont need to record line number
    IS_EXIST = 0
    with open('/etc/pam.d/su', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.search('auth', line) and re.search('pam_wheel.so', line) and re.search('group=wheel', line):
                IS_EXIST = 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC23\n")
        logger.warning("WRN_C23: %s", WRN_C23)
        Display("- There is no pam_wheel set, check warning","WARNING")
    else:
        logger.info("There have pam_wheel set, check OK")
        Display("- Check the pam.d/su setting...", "OK")

