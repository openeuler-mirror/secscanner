import logging
import os
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C01_motd():
    logger = logging.getLogger("secscanner")
    InsertSection("check /etc/motd banner")
    if (os.path.exists("/etc/motd") and os.path.getsize("/etc/motd")):
        logger.info("Has /etc/motd set, checking ok")
        # Display("--indent 2 --text - Has /etc/motd set...  --result OK --color GREEN")
        Display("- Has /etc/motd set...",  "OK")
        # ADDHP 1 1
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC01\n")
        logger.info("WRN_C01: %s", WRN_C01)
        logger.warning("Suggestion: %s", SUG_C01)
        Display("- No /etc/motd set...", "WARNING")
        # ADDHP 0 1
