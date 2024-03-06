import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")



def C18_syslogKern():
    InsertSection("check if record the kernel warn")
    SYSLOG_CONF = ['/etc/rsyslog.conf']
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
                logger.warning("WRN_C18: %s", WRN_C18)
                logger.warning("SUG_C18: %s", SUG_C18)
                Display("- Check if there have kern.warning set...", "WARNING")
            else:
                logger.info("The security audit modle kern.warning is set, checking OK")
                Display("- Check if there have kern.warning set...","OK")
        else:
            Display(f"- file {i} does not exist...", "SKIPPED")
