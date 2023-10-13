import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C26_setaliases():
    InsertSection("check ls and rm aliases")
    set_ls = 'unset'
    set_rm = 'unset'
    with open('/root/.bashrc', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('alias ls', line) and not re.match('^#|^$', line):
                set_ls = 'set'
                temp = line.strip('\n').split('=')
                if len(temp) == 2 and temp[1] == '\'ls -al\'':
                    set_ls = 'right'

    with open('/root/.bashrc', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('alias rm', line) and not re.match('^#|^$', line):
                set_rm = 'set'
                temp = line.strip('\n').split('=')
                if len(temp) == 2 and temp[1] == '\'rm -i\'':
                    set_rm = 'right'

    if set_ls == 'unset' and set_rm == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC26\n")
        logger.warning("WRN_C26_01: %s", WRN_C26_01)
        logger.warning("SUG_C26: %s", SUG_C26)
        Display("- No ls and rm aliases set...", "WARNING")
    elif set_ls == 'right' and set_rm == 'right':
        logger.info("Has ls and rm aliases set, checking OK")
        Display("- Check the ls and rm aliases set...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC26\n")
        logger.warning("WRN_C26_02: %s", WRN_C26_02)
        logger.warning("SUG_C26: %s", SUG_C26)
        Display("- Wrong ls and rm aliases set...", "WARNING")
