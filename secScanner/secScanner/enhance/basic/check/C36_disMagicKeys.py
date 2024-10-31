import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")


def C36_disMagicKeys():
    InsertSection("check disable magic keys")
    sysrq_set = 'unset'
    if os.path.exists('/etc/sysctl.conf'):
        with open("/etc/sysctl.conf", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('kernel.sysrq', line) and not re.match('^#|^$', line):
                    sysrq_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == '0\n':
                        sysrq_set = 'right'
        
        if sysrq_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC36\n")
            logger.warning("WRN_C36_01: %s", WRN_C36_01)
            logger.warning("SUG_C36: %s", SUG_C36)
            Display("- No disable magic keys set...", "WARNING")
        elif sysrq_set == 'right':
            logger.info("Has disable magic keys set, checking OK")
            Display("- Check disable magic keys set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC36\n")
            logger.warning("WRN_C36_02: %s", WRN_C36_02)
            logger.warning("SUG_C36: %s", SUG_C36)
            Display("- Wrong disable magic keys set...", "WARNING")
    else:
        Display("- No path /etc/sysctl.conf exists", "WARNING")
