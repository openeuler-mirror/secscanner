import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C26_disableUnUsedaliases():
    logger = logging.getLogger("secscanner")
    InsertSection("check disable the unused aliases")
    COUNT = 0
    UNUSED_ALIASES_VAL = seconf.get('advance', 'unused_aliases_value').split()
    FILE_NAME = ['/etc/aliases', '/etc/mail/aliases']
    undisabled_aliases = ''
    for f in FILE_NAME:
        if os.path.exists(f):
            with open(f, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if not re.match('^#', line):
                        temp = line.split(':', -1)
                        if len(temp) == 2 and (temp[0] in UNUSED_ALIASES_VAL):
                            COUNT = COUNT + 1
                            undisabled_aliases = undisabled_aliases + temp[0]

    if COUNT > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC26\n")
        logger.warning(f"WRN_C26: These users {undisabled_aliases} should disable")
        logger.warning("SUG_C26: %s", SUG_C26)
        Display("- Check if there have unused aliases...", "WARNING")
    else:
        logger.info("All unused aliases are locked, checking ok")
        Display("- Check if unused aliases are locked...", "OK")

