import logging
import os
import re
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C27_syslogProperty():
    InsertSection("check log file property")
    SYS_LOGFILE = ['/etc/rsyslog.conf']
    if os.path.exists('/etc/rsyslog.conf'):
        with open('/etc/rsyslog.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.search('/var/log', line) and (not re.match('^#|^$', line)):
                    temp = line.split()
                    if len(temp) == 2 and re.match('^/var', temp[1]):
                        SYS_LOGFILE.append(temp[1])

        for f in SYS_LOGFILE:
            if os.path.exists(f):
                ret, result = subprocess.getstatusoutput(f'ls -al {f}')
                result = result.split()
                if ('rw-------' in result[0]):
                    Display(f"- check if {f} property is 600 ...", "OK")
                else:
                    with open(RESULT_FILE, "a") as file:
                        file.write("\nC27\n")
                    logger.warning("WRN_C27: %s", WRN_C27)
                    logger.warning("SUG_C27: %s", SUG_C27)
                    Display(f"- Check if {f} property is not 600...", "WARNING")
    else:
        Display(f"- file '/etc/rsyslog.conf' does not exist...", "SKIPPED")
