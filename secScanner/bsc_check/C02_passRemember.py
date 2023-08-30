import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *
from secScanner.lib.TextInfo import *

def C02_passRemember():
    logger = logging.getLogger("secscanner")
    InsertSection("check passwd Remember times")
    SET_VAL = []
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search('pam_unix.so', line) and re.search('remember=', line):
                regex = r'(?<=remember=).[0-9]*'
                SET_VAL = re.findall(regex, line)
    if SET_VAL == []:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC02\n")
        logger.warning("WRN_C02: %s", WRN_C02_01)
        logger.warning("Suggestion: %s", SUG_C02)
        Display("- No Password Remember set...", "WARNING")
    elif SET_VAL[0] > '4':
        logger.info("has passwd Remember times set, checking ok")
        Display("- Has Password Remember set...", "OK")
    elif SET_VAL[0] <= '4' and SET_VAL[0] >= '0':
        logger.warning("WRN_C02: %s", WRN_C02_02)
        Display("- Password Remember times is not right...", "WARNING")
    else:
        Display("- Password Remember times is invalid...", "WARNING")
