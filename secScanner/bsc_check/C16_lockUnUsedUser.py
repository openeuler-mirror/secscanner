import logging
import os
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C16_lockUnUsedUser():
    InsertSection("check the unused user")
    UnUsed = ['adm', 'lp', 'sync', 'shutdown', 'halt', 'news', 'uucp', 'operator', 'games', 'nobody', 'rpm', 'smmsp']
    ERROR_USER = ''
    with open("/etc/shadow", "r") as file:
        lines = file.readlines()
        for line in lines:
            temp = line.split(':', -1)
            if temp[0] in UnUsed:
                ERROR_USER = ERROR_USER + temp[0] + ' '
    if len(ERROR_USER) > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC16\n")
        logger.warning(f"WRN_C16: These users: {ERROR_USER} should lock")
        logger.warning("SUG_C16: %s", SUG_C16)
        Display("- Check if there have unused user...", "WARNING")
    else:
        logger.info("All unused user is locked, checking ok")
        Display("- Check if there have unused user...", "OK")
