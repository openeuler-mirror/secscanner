import logging
import re
import os
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C13_restrictFTPdir():
    InsertSection("check the ftp restrict directories")
    chroot_set = 'unset'
    chrootlist_set = 'unset'
    listfile_set = 'unset'
    if os.path.exists('/etc/vsftpd/vsftpd.conf'):
        with open('/etc/vsftpd/vsftpd.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('chroot_local_user', line) and not re.match('^#|^$', line):
                    chroot_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == 'YES\n':
                        chroot_set = 'right'
                if re.match('chroot_list_enable', line) and not re.match('^#|^$', line):
                    chrootlist_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == 'YES\n':
                        chrootlist_set = 'right'
                if re.match('chroot_list_file', line) and not re.match('^#|^$', line):
                    listfile_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == '/etc/vsftpd/chroot_list\n':
                        listfile_set = 'right'


        if chroot_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC30\n")
            logger.warning("WRN_C13_01: %s", WRN_C13_01)
            logger.warning("SUG_C13: %s", SUG_C13)
            Display("- No ftp restrict directories set...", "WARNING")
        elif chroot_set == 'right' and chrootlist_set == 'right' and listfile_set == 'right':
            logger.info("Has ftp restrict directories set, checking OK")
            Display("- Check the ftp restrict directories...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC30\n")
            logger.warning("WRN_C13_02: %s", WRN_C13_02)
            logger.warning("SUG_C13: %s", SUG_C13)
            Display("- Wrong ftp restrict directories set...", "WARNING")
    else:
        Display("- Path /etc/vsftpd/vsftpd.conf not exists...", "WARNING")
