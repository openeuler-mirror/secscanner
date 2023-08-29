import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C13_sshProtocol():
    logger = logging.getLogger("secscanner")

    InsertSection("check the ssh protocol")
    PROTOCOL_VAL = 'unset' #set 'unset' in case of no 'Protocol' in file
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('Protocol', line) and (not re.match('^#|^$', line)):
                PROTOCOL_VAL = 'wrong' #set 'wrong' in case of nothing after 'Protocol'
                if re.search('2', line):
                    PROTOCOL_VAL = 'right'
    if PROTOCOL_VAL == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC13\n")
        logger.info("WRN_C13_01: %s", WRN_C13_01)
        logger.warning("Suggestion: %s", SUG_C13)
        Display("- No ssh protocol config set...", "WARNING")
    elif PROTOCOL_VAL == 'right':
        logger.info("Has ssh protocol set, checking ok")
        Display("- Check the ssh protocol...", "OK")
    else:
        logger.info("WRN_C13_02: %s", WRN_C13_02)
        logger.warning("Suggestion: %s", SUG_C13)
        Display("- Wrong ssh protocol config set...", "WARNING")

