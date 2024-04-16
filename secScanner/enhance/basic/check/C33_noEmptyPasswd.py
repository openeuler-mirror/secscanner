import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C33_noEmptyPasswd():
    InsertSection("check the ssh permit empty passwd")
    CONFIG_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('PermitEmptyPasswords', line) and not re.match('^#|^$', line):
                CONFIG_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'no':
                    CONFIG_SET = 'right'

    if CONFIG_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC33\n")
        logger.warning("WRN_C33_01: %s", WRN_C33_01)
        logger.warning("SUG_C33: %s", SUG_C33)
        Display("- No ssh PermitEmptyPasswords config set...", "WARNING")
    elif CONFIG_SET == 'right':
        logger.info("Has ssh PermitEmptyPasswords set, checking OK")
        Display("- Check the ssh PermitEmptyPasswords...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC33\n")
        logger.warning("WRN_C33_02: %s", WRN_C33_02)
        logger.warning("SUG_C33: %s", SUG_C33)
        Display("- Wrong ssh PermitEmptyPasswords config set...", "WARNING")
