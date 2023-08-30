import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C24_noOneSU():
    logger = logging.getLogger("secscanner")
    InsertSection("check if permit user can su to root")
    # LINE_NUMBER = 0 # dont need to record line number
    IS_EXIST = 0
    with open('/etc/pam.d/su', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('pam_wheel.so', line) and re.search('\"group=wheel\"', line):
                IS_EXIST = 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC24\n")
        logger.info(f"WRN_C24: %s :", WRN_C24)
        logger.warning("Suggestion: %s", SUG_C24)
        Display("- Check the pam.d/su setting...", "WARNING")
        Display("- There is no pam_wheel set, check warning")
    else:
        logger.info("There have pam_wheel set, check OK")
        Display("- Check the pam.d/su setting...", "OK")

