import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C20_syslogAuth():
    InsertSection("check if record the auth events")
    SYSLOG_CONF = ['/etc/rsyslog.conf']
    count = 0
    for i in SYSLOG_CONF:
        if os.path.isfile(i) and os.path.getsize(i) > 0:
            #check file exist and not empty
            with open(i, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('auth.none', line) and re.search('/var/log/', line) and not re.match('#', line):
                        count = count + 1
            if count == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC20\n")
                logger.warning("WRN_C20: %s", WRN_C20)
                logger.warning("SUG_C20: %s", SUG_C20)
                Display("- Check if there have auth.none set...", "WARNING")
            else:
                logger.info("The security audit module auth.none is set, checking OK")
                Display("- Check if there have auth.none set...", "OK")
        else:
            Display(f"- file {i} does not exist...", "SKIPPED")
