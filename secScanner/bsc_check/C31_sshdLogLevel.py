import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
def C51_sshdLogLevel():
    logger = logging.getLogger("secscanner")
    InsertSection("check the ssh loglevel")
    LOGLEVEL_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('LogLevel', line) and not re.match('^#|^$', line):
                LOGLEVEL_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'VERBOSE':
                    LOGLEVEL_SET = 'right'


    if LOGLEVEL_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC51\n")
        logger.info(f"WRN_C51_01: %s :", WRN_C51_01)
        logger.warning("Suggestion: %s", SUG_C51)
        Display("- No ssh loglevel config set...", "WARNING")
    elif LOGLEVEL_SET == 'right':
        logger.info("Has ssh loglevel set, checking OK")
        Display("- Check the ssh loglevel...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC51\n")
        logger.info(f"WRN_C51_02: %s :", WRN_C51_02)
        logger.warning("Suggestion: %s", SUG_C50)
        Display("- Wrong ssh loglevel config set...", "WARNING")