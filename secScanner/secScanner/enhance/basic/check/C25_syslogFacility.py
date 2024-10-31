import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C25_syslogFacility():
    InsertSection("check the ssh syslogfacility")
    SYSLOG_FACILITY = 'unset'
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if (not re.match('^#|^$', line) and re.search('SyslogFacility', line) and re.search('AUTH', line)):
                SYSLOG_FACILITY = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'AUTH':
                    SYSLOG_FACILITY = 'right'
    if SYSLOG_FACILITY == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC25\n")
        logger.warning("WRN_C25_01: %s", WRN_C25_01)
        logger.warning("SUG_C25: %s", SUG_C25)
        Display("- No ssh syslogfacility config set...", "WARNING")
    elif SYSLOG_FACILITY == 'wrong':
        logger.warning("WRN_C25_02: %s", WRN_C25_02)
        logger.warning("SUG_C25: %s", SUG_C25)
        Display("- Wrong ssh syslogfacility config set...", "WARNING")
    else:
        logger.info("Has ssh syslogfacility set, checking ok")
        Display("- Check the ssh syslogfacility...", "OK")
