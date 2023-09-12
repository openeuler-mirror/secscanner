import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C22_resourceLimit():
    InsertSection("check the resource limit")
    SOFT_CORE = 0
    HARD_CORE = 0
    with open("/etc/security/limits.conf", "r") as file:
        lines = file.readlines()
        for line in lines:
            if (not re.match('^#|^$', line)) and re.search('soft', line) and re.search('core', line):
                SOFT_CORE = 1
                temp = line.split()
                VALUE = temp[3]
                if VALUE == '0':
                    logger.info("The system soft core limit is '0, checking ok")
                    Display("- Check if the soft core limits is ok...", "OK")
                else:
                    with open(RESULT_FILE, "a") as file:
                        file.write("\nC22\n")
                    logger.warning("WRN_C22_01: %s", WRN_C22_01)
                    logger.warning("SUG_C22_01: %s", SUG_C22_01)
                    Display("- Check if the soft core limits is ok...", "WARNING")


            if (not re.match('^#|^$', line)) and re.search('hard', line) and re.search('core', line):
                HARD_CORE = 1
                temp = line.split()
                VALUE = temp[3]
                if VALUE == '0':
                    logger.info("The system hard core limit is '0, checking ok")
                    Display("- Check if the hard core limits is ok...", "OK")
                else:
                    with open(RESULT_FILE, "a") as file:
                        file.write("\nC22\n")
                    logger.warning("WRN_C22_03: %s", WRN_C22_03)
                    logger.warning("SUG_C22_02: %s", SUG_C22_02)
                    Display("- Check if the hard core limits is ok...", "WARNING")
    if SOFT_CORE == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC22\n")
        logger.warning("WRN_C22_02: %s", WRN_C22_02)
        logger.warning("SUG_C22_01: %s", SUG_C22_01)
        Display("- This system has no soft core limit set...", "WARNING")
    if HARD_CORE == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC22\n")
        logger.warning("WRN_C22_04: %s", WRN_C22_04)
        logger.warning("SUG_C22_02: %s", SUG_C22_02)
        Display("- This system has no hard core limit set...", "WARNING")
