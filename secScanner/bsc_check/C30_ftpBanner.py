import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C30_ftpBanner():
    InsertSection("check the ftp banner")
    ftpBanner_set = 'unset'
    with open('/etc/vsftpd/vsftpd.conf', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('ftpd_banner', line) and not re.match('^#|^$', line):
                ftpBanner_set = 'wrong'
                temp = line.split('=')
                if len(temp) == 2 and temp[1] == ('Authorized users only. All activity may be '
                                                  'monitored and reported.\n'):
                    ftpBanner_set = 'right'
    if ftpBanner_set == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC30\n")
        logger.warning("WRN_C30_01: %s", WRN_C30_01)
        logger.warning("SUG_C30: %s", SUG_C30)
        Display("- No ftp banner config set...", "WARNING")
    elif ftpBanner_set == 'right':
        logger.info("Has ftp banner set, checking OK")
        Display("- Check the ftp banner set...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC30\n")
        logger.warning("WRN_C30_02: %s", WRN_C30_02)
        logger.warning("SUG_C30: %s", SUG_C30)
        Display("- Wrong ftp banner config set...", "WARNING")
