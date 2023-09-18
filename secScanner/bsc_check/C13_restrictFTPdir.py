import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C13_restrictFTPdir():
    InsertSection("check the ftp restrict directories")
    restrictFTPdir_set = 'unset'
    with open('/etc/vsftpd/vsftpd.conf', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('chroot_local_user', line) and not re.match('^#|^$', line):
                restrictFTPdir_set = 'wrong'
                temp = line.split('=')
                if len(temp) == 2 and temp[1] == 'YES\n':
                    restrictFTPdir_set = 'right'

    if restrictFTPdir_set == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC30\n")
        logger.warning("WRN_C13_01: %s", WRN_C13_01)
        logger.warning("SUG_C13: %s", SUG_C13)
        Display("- No ftp restrict directories set...", "WARNING")
    elif restrictFTPdir_set == 'right':
        logger.info("Has ftp restrict directories set, checking OK")
        Display("- Check the ftp restrict directories...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC30\n")
        logger.warning("WRN_C13_02: %s", WRN_C13_02)
        logger.warning("SUG_C13: %s", SUG_C13)
        Display("- Wrong ftp restrict directories set...", "WARNING")
