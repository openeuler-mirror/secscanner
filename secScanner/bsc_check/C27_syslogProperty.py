import logging
import os
import re
import subprocess
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C27_syslogProperty():
    logger = logging.getLogger("secscanner")
    InsertSection("check log file property")
    SYS_LOGFILE = []
    with open('/etc/rsyslog.conf', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.search('/var/log', line) and (not re.match('^#|^$', line)):
                temp = line.split()
                if len(temp) == 2 and re.match('^/var', temp[1]):
                    SYS_LOGFILE.append(temp[1])

    for f in SYS_LOGFILE:
        if os.path.exists(f):
            ilog_perm = subprocess.run(['ls', '-al', f], stdout = subprocess.PIPE)
            result = ilog_perm.stdout.split()
            if(b'rw-------' in result[0]):
                Display(f"- check if {f} property is 600 or not...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC27\n")
                logger.warning("WRN_C27: %s", WRN_C27)
                logger.warning("SUG_C27: %s", SUG_C27)
                Display(f"- Check if {f} property is 600 or not...", "WARNING")


