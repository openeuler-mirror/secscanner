import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C05_icmpLimit():
    logger = logging.getLogger("secscanner")
    InsertSection("check icmp redirect limit")
    ICMP_EXIST = 0
    with open("/etc/sysctl.conf", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('net.ipv4.conf.all.accept_redirects=0', line) and (not re.match('#', line)) and (not re.match('$', line)):
                ICMP_EXIST = 1

    if ICMP_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC05\n")
        logger.warning("WRN_C05: %s", WRN_C05)
        logger.warning("SUG_C05: %s", SUG_C05)
        Display("- Wrong icmp limit set...", "WARNING")
    else:
        logger.info("Has icmp redirect limit set, checking ok")
        Display("- Has icmp redirect limit set...", "OK")
