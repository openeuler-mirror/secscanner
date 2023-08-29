import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
SYSLOG_CONF = ['/etc/rsyslog.conf', '/etc/syslog.conf']
def C17_syslogLogin():
    logger = logging.getLogger("secscanner")
    InsertSection("check if record the user login events")
    count = 0
    for i in SYSLOG_CONF:
        if os.path.isfile(i) and os.path.getsize(i) > 0:
            #check file exist and not empty
            with open(i, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('authpriv.info', line) and re.search('/var/log/', line) and not re.match('#', line):
                        count = count + 1
            if count == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC17\n")
                logger.info(f"WRN_C17: %s :", WRN_C17)
                logger.warning("Suggestion: %s", SUG_C17)
                Display("- Check if there have authpriv.info set...", "WARNING")
            else:
                logger.info("The security audit modle authpriv.info is set, checking OK")
                Display("- Check if there have authpriv.info set...", "OK")