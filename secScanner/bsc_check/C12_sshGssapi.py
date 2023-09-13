import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C12_sshGssapi():
    InsertSection("check the ssh gssapi")
    GSSAPI_VAL = ''
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('^GSSAPIAuthentication', line) and (not re.match('^#|^$', line)):
                temp = line.split()
                if len(temp) == 2:  # check if there is only one word after GSSAPIAuthentication
                    GSSAPI_VAL = temp[1]  # umask 022 UMASK_VAL: 022
    if GSSAPI_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC12\n")
        logger.warning("WRN_C12_02: %s", WRN_C12_02)
        logger.warning("SUG_C12: %s", SUG_C12)
        Display("- No ssh gssapi config set...", "WARNING")
    elif GSSAPI_VAL.lower() == 'no':
        logger.warning("Has ssh gssapi set, checking ok")
        Display("- Check the ssh gssapi...", "OK")
    else:
        logger.warning("WRN_C12_01: %s", WRN_C12_01)
        logger.warning("SUG_C12: %s", SUG_C12)
        Display("- Wrong ssh gssapi config set...", "WARNING")

