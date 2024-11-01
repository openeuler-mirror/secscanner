import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")

def C06_umask():
    InsertSection("check the file umask value ")
    UMASK_VAL = ''
    with open("/etc/profile", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.search('mask', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2:#check if there is only one number after umask
                    UMASK_VAL = temp[1] # umask 022 UMASK_VAL: 022

    if UMASK_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC06\n")
        logger.warning("WRN_C06: %s", WRN_C06)
        logger.warning("SUG_C06: %s", SUG_C06)
        Display("- No umask set...", "WARNING")
    elif UMASK_VAL < '027':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC06\n")
        logger.warning("WRN_C06: %s", WRN_C06)
        logger.warning("SUG_C06: %s", SUG_C06)
        Display("- Wrong umask set...", "WARNING")
    else:
        logger.info("Has right umask set, checking ok")
        Display("- Has right umask set...", "OK")
