import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
def C50_initUserPath():
    logger = logging.getLogger("secscanner")
    InsertSection("check the ALWAYS_SET_PATH set in /etc/login.defs")
    ALWAYS_SET = 'unset'
    with open('/etc/login.defs', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('ALWAYS_SET_PATH', line) and not re.match('^#|^$', line):
                ALWAYS_SET = 'wrong'
                if re.search('yes', line):
                    ALWAYS_SET = 'right'


    if ALWAYS_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC50\n")
        logger.info(f"WRN_C50_01: %s :", WRN_C50_01)
        logger.warning("Suggestion: %s", SUG_C50)
        Display("- No ALWAYS_SET_PATH config set...", "WARNING")
    elif ALWAYS_SET == 'right':
        logger.info("Has ALWAYS_SET_PATH set, checking OK")
        Display("- Check the ALWAYS_SET_PATH...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC50\n")
        logger.info(f"WRN_C50_02: %s :", WRN_C50_02)
        logger.warning("Suggestion: %s", SUG_C50)
        Display("- Wrong ALWAYS_SET_PATH config set...", "WARNING")