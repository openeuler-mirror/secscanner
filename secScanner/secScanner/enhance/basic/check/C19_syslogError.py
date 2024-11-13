import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C19_syslogError():
    InsertSection("check if record the error events")
    SYSLOG_CONF = ['/etc/rsyslog.conf']
    count = 0
    for i in SYSLOG_CONF:
        if os.path.isfile(i) and os.path.getsize(i) > 0:
            #check file exist and not empty
            with open(i, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('\\*.err', line) and re.search('/var/log/', line) and not re.match('#', line):
                        count = count + 1
            if count == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC19\n")
                logger.warning("WRN_C19: %s", WRN_C19)
                logger.warning("SUG_C19: %s", SUG_C19)
                Display("- Check if there have *.err set...", "WARNING")
            else:
                logger.info("The security audit module *.err is set, checking OK")
                Display("- Check if there have *.err set...", "OK")
        else:
            Display(f"- file {i} does not exist...", "SKIPPED")
