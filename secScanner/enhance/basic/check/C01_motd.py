import logging
import os
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")

def C01_motd():
    InsertSection("check /etc/motd banner")
    if os.path.exists("/etc/motd") and os.path.getsize("/etc/motd"):
        logger.info("Has /etc/motd set, checking ok")
        Display("- Has /etc/motd set...",  "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC01\n")
        logger.warning("WRN_C01: %s", WRN_C01)
        logger.warning("SUG_C01: %s", SUG_C01)
        Display("- No /etc/motd set...", "WARNING")
