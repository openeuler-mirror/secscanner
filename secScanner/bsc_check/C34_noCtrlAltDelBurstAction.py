import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C34_noCtrlAltDelBurstAction():
    InsertSection("check the system CtrlAltDel Burst Action")
    CONFIG_SET = 'unset'

    if not os.path.exists("/etc/systemd/system/ctrl-alt-del.target_bak") and not os.path.exists("/usr/lib/systemd/system/ctrl-alt-del.target"):
        with open('/etc/systemd/system.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('CtrlAltDelBurstAction', line) and not re.match('^#|^$', line):
                    CONFIG_SET = 'wrong'
                    temp = line.split("=")
                    if len(temp) == 2 and temp[1] == 'none':
                        CONFIGL_SET = 'right'

    if CONFIG_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC34\n")
        logger.warning("WRN_C34_01: %s", WRN_C34_01)
        logger.warning("SUG_C34: %s", SUG_C34)
        Display("- No system CtrlAltDel burst action config set...", "WARNING")
    elif CONFIG_SET == 'right':
        logger.info("Has system CtrlAltDel burst action set, checking OK")
        Display("- Check the system CtrlAltDel burst action...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC34\n")
        logger.warning("WRN_C34_02: %s", WRN_C34_02)
        logger.warning("SUG_C34: %s", SUG_C34)
        Display("- Wrong system CtrlAltDel burst action config set...", "WARNING")
