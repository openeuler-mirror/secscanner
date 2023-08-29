import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
def C06_umask():
    logger = logging.getLogger("secscanner")

    InsertSection("check umask")

    # cat /etc/profile|grep mask|grep -v "#" | awk -F " " '{print $2}'|tail -1 | while read val
    # read the last val
    UMASK_VAL = ''
    with open("/etc/profile", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.search('mask', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2:#check if there is only one number after umask
                    UMASK_VAL = temp[1] # umask 022 UMASK_VAL: 022
    # after "for line in lines:" , UMASK_VAL is the last umask value in /etc/profile

    if UMASK_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC06\n")
        logger.info("WRN_C06: %s", WRN_C06)
        logger.warning("Suggestion: %s", SUG_C06)
        Display("- No umask set...", "WARNING")
    elif UMASK_VAL < '027':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC06\n")
        logger.info("WRN_C06: %s", WRN_C06)
        logger.warning("Suggestion: %s", SUG_C06)
        Display("- Wrong umask set...", "WARNING")
    else:
        logger.info("Has right umask set, checking ok")
        Display("- Has right umask set...", "OK")
