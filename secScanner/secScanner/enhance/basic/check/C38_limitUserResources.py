import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C38_limitUserResources():
    InsertSection("check limit of system resources")
    set01 = False
    set02 = False
    set03 = False
    set04 = False
    set05 = False
    set_pam = False
    with open("/etc/security/limits.conf", "r") as file:
        lines = file.readlines()
        for line in lines:
            if (not re.match('#|$', line)) and re.search('soft', line) and re.search('stack', line):
                set01 = True
            if (not re.match('#|$', line)) and re.search('hard', line) and re.search('stack', line):
                set02 = True
            if (not re.match('#|$', line)) and re.search('hard', line) and re.search('rss', line):
                set03 = True
            if (not re.match('#|$', line)) and re.search('hard', line) and re.search('nproc', line):
                set04 = True
            if (not re.match('#|$', line)) and re.search('hard', line) and re.search('maxlogin', line):
                set05 = True
    
    with open('/etc/pam.d/login', 'r') as read_file:
        lines = read_file.readlines()
        for line in lines:
            if (not re.match('#|$', line)) and re.match('session', line) and re.search('/lib/security/pam_limits.so', line):
                set_pam = True

    if not (set01 and set02 and set03 and set04 and set05 and set_pam):
        with open(RESULT_FILE, "a") as file:
            file.write("\nC38\n")
        logger.warning("WRN_C38: %s", WRN_C38)
        logger.warning("SUG_C38: %s", SUG_C38)
        Display("- This system has no limit of system resources...", "WARNING")
    else:
        logger.info("The system has limit of system resources, checking ok")
        Display("- Check if the limit of system resources is ok...", "OK")
