import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
SYSLOG_CONF = ['/etc/rsyslog.conf', '/etc/syslog.conf']
def C18_syslogKern():
    logger = logging.getLogger("secscanner")
    InsertSection("check if record the kernel warn")
    count = 0
    for i in SYSLOG_CONF:
        if os.path.isfile(i) and os.path.getsize(i) > 0:
            #check file exist and not empty
            with open(i, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('kern.warning', line) and re.search('/var/log/', line) and not re.match('#', line):
                        count = count + 1
            if count == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC18\n")
                logger.warning(f"WRN_C18: %s", WRN_C18)
                logger.warning("Suggestion: %s", SUG_C18)
                Display("- Check if there have kern.warn set...", "WARNING")
            else:
                logger.info("The security audit modle kern.warn is set, checking OK")
                Display("- Check if there have kern.warn set...","OK")
