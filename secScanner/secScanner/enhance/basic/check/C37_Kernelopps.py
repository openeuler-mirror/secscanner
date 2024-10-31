import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")


def C37_Kernelopps():
    InsertSection("check kernel panic on oops set")
    kerneloops_set = 'unset'
    if os.path.exists('/etc/sysctl.conf'):
        with open("/etc/sysctl.conf", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('kernel.panic_on_oops', line) and not re.match('^#|^$', line):
                    kerneloops_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == '1\n':
                        kerneloops_set = 'right'

        rclocal_set = False
        if os.path.exists('/etc/rc.local'):
            with open('/etc/rc.local', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                        rclocal_set = True
        else:
            Display("- No path /etc/rc.local exists", "WARNING")

        if kerneloops_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC37\n")
            logger.warning("WRN_C37_01: %s", WRN_C37_01)
            logger.warning("SUG_C37: %s", SUG_C37)
            Display("- No kernel panic on oops set...", "WARNING")
        elif kerneloops_set == 'right' and rclocal_set:
            logger.info("Has kernel panic on oops set set, checking OK")
            Display("- Check kernel panic on oops set set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC37\n")
            logger.warning("WRN_C37_02: %s", WRN_C37_02)
            logger.warning("SUG_C37: %s", SUG_C37)
            Display("- Wrong kernel panic on oops set set...", "WARNING")
    else:
        Display("- No path /etc/sysctl.conf exists", "WARNING")
