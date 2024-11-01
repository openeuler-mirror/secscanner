import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")


def C14_sshRootDenie():

    InsertSection("check the ssh root denie")
    OS_DISTRO = get_value("OS_DISTRO")
    if OS_DISTRO == '7':
        IS_EXIST = 0
        with open('/etc/securetty', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.search('pts/', line) and not re.match('^#|^$', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            Display("- Check the telnet deny...", "OK")
        else:
            Display("- Wrong Telnet Denie set...", "WARNING")

### check the SSH Root Denie
    SSH_ROOT_DENIE_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('PermitRootLogin', line) and (not re.match('^#|^$', line)):
                SSH_ROOT_DENIE_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'no':
                    SSH_ROOT_DENIE_SET = 'right'


    if SSH_ROOT_DENIE_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC14\n")
        logger.warning("WRN_C14_01: %s", WRN_C14_01)
        logger.warning("SUG_C14: %s", SUG_C14)
        Display("- No ssh Root denie set...", "WARNING")
    elif SSH_ROOT_DENIE_SET == 'right':
        logger.info("Has ssh Root denie set, checking OK")
        Display("- Check the ssh Root denie...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC14\n")
        logger.warning(f"WRN_C14_02: %s", WRN_C14_02)
        logger.warning("SUG_C14: %s", SUG_C14)
        Display("- Wrong ssh Root denie set...", "WARNING")
