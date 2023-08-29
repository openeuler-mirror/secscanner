import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
def S23_vsftpSecure():
    SET_VSFTP_SECURITY = seconf.get('basic', 'set_vsftp_security')
    logger = logging.getLogger("secscanner")
    InsertSection("Set the vsftp...")
    if SET_VSFTP_SECURITY == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            if not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
                shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
            IS_EXIST = 0
            IS_EXIST2 = 0
            IS_EXIST3 = 0
            IS_EXIST4 = 0
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('anonymous_enable', line):
                        IS_EXIST = 1
                    if (not re.match('#|$', line)) and re.search('ftpd_banner', line):
                        IS_EXIST2 = 1
                    if (not re.match('#|$', line)) and re.search('userlist_enable', line):
                        IS_EXIST3 = 1
                    if (not re.match('#|$', line)) and re.search('userlist_deny', line):
                        IS_EXIST4 = 1
            # -----------------set anonymous_enable=NO------------------
            if IS_EXIST == 0:
                with open('/etc/vsftpd/vsftpd.conf', 'a') as add_file:
                    add_file.write("\nanonymous_enable=NO\n")
            else:
                with open('/etc/vsftpd/vsftpd.conf', 'w') as write_file:
                    for line in lines:
                        if re.search('anonymous_enable', line):
                            write_file.write("anonymous_enable=NO\n")
                        else:
                            write_file.write(line)
            # -----------------set vsftp banner------------------
            if IS_EXIST2 == 0:
                with open('/etc/vsftpd/vsftpd.conf', 'a') as add_file:
                    add_file.write("\nftpd_banner=\"ATTENTION:You have logged onto a secured server..All accesses logged.\"\n")
            else:
                logger.info("has ftpd_banner set, passing")
            # -----------------restrict user ftp login------------------
            if IS_EXIST3 == 0:
                with open('/etc/vsftpd/vsftpd.conf', 'a') as add_file:
                    add_file.write("\nuserlist_enable=YES\n")
            else:
                with open('/etc/vsftpd/vsftpd.conf', 'w') as write_file:
                    for line in lines:
                        if re.search('userlist_enable', line):
                            write_file.write("userlist_enable=YES\n")
                        else:
                            write_file.write(line)

            if IS_EXIST4 == 0:
                with open('/etc/vsftpd/vsftpd.conf', 'a') as add_file:
                    add_file.write("\nuserlist_deny=NO\n")
            else:
                with open('/etc/vsftpd/vsftpd.conf', 'w') as write_file:
                    for line in lines:
                        if re.search('userlist_deny', line):
                            write_file.write("userlist_deny=NO\n")
                        else:
                            write_file.write(line)
            # -----------------restrict user ftp login------------------
            IS_EXIST = 0
            with open('/etc/vsftpd/ftpusers', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('root', line):
                        IS_EXIST = 1
            if IS_EXIST == 0:
                with open('/etc/vsftpd/ftpusers', 'a') as add_file:
                    add_file.write("\nroot\n")

            Display(f"- Config the vsftp, make it safe...", "FINISHED")

        else:
            logger.info("/etc/vsftpd/vsftpd.conf not found, or it does not installed")
            Display(f"- No vsftpd.conf found, maybe vsftp not installed...", "SKIPPED")
    else:
        Display(f"- Skip set vsftp security due to config file...", "SKIPPING")

