import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
import subprocess
logger = logging.getLogger("secscanner")


def S13_restrictFTPdir():
    set_ftp_restrictdir = seconf.get('advance', 'set_ftp_restrictdir')
    InsertSection("Set the restrict directories of ftp...")
    if set_ftp_restrictdir == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf') and not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
            shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
            # -----------------set the restrictFTPdir----------------
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            with open('/etc/vsftpd/vsftpd.conf', 'r+') as f:
                lines = f.readlines()
                chroot_exists = False
                chrootlist_exists = False
                chrootlist_file = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#chroot_local_user"):
                        lines[i] = lines[i].replace("#", "")
                        if not re.search('YES', line):
                            lines[i] = "chroot_local_user=YES\n"
                        chroot_exists = True
                        #break
                    elif line.strip().startswith("chroot_local_user"):
                        chroot_exists = True
                        if not re.search('YES', line):
                            lines[i] = "chroot_local_user=YES\n"
                        #break

                    if line.strip().startswith("#chroot_list_enable=YES"):
                        lines[i] = lines[i].replace("#", "")
                        if not re.search('YES', line):
                            lines[i] = "chroot_list_enable=YES\n"
                        chrootlist_exists = True
                        #break
                    elif line.strip().startswith("chroot_list_enable"):
                        chrootlist_exists = True
                        if not re.search('YES', line):
                            lines[i] = "chroot_list_enable=YES\n"
                        #break

                    if line.strip().startswith("#chroot_list_file=/etc/vsftpd/chroot_list"):
                        lines[i] = lines[i].replace("#", "")
                        if not re.search('YES', line):
                            lines[i] = "chroot_list_file=/etc/vsftpd/chroot_list\n"
                        chrootlist_file = True
                        break
                    elif line.strip().startswith("chroot_list_file"):
                        chrootlist_file = True
                        if not re.search('/etc/vsftpd/chroot_list', line):
                            lines[i] = "chroot_list_file=/etc/vsftpd/chroot_list\n"
                        break

                if not chroot_exists:
                    lines.append("chroot_local_user=YES\n")
                if not chrootlist_exists:
                    lines.append("chroot_list_enable=YES\n")
                if not chrootlist_file:
                    lines.append("chroot_list_file=/etc/vsftpd/chroot_list\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            chroot_check = False
            chrootlist_check = False
            listfile_check = False
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('chroot_local_user', line):
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'chroot_local_user' and temp[1] == 'YES':
                            chroot_check = True
                    if (not re.match('#|$', line)) and re.search('chroot_list_enable', line):
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'chroot_list_enable' and temp[1] == 'YES':
                            chrootlist_check = True
                    if (not re.match('#|$', line)) and re.search('chroot_list_file', line):
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'chroot_list_file' and temp[1] == '/etc/vsftpd/chroot_list':
                            listfile_check = True

            if chroot_check and chrootlist_check and listfile_check:
                ret, result = subprocess.getstatusoutput('systemctl is-active vsftpd')
                if ret != 0:
                    flag, out = subprocess.getstatusoutput('systemctl start vsftpd')
                    if flag != 0:
                        logger.warning('Start vsftpd failed')
                        Display("- Start vsftpd service failed...", "FAILED")
                        sys.exit(1)
                else:
                    flag, out = subprocess.getstatusoutput('systemctl restart vsftpd')
                    if flag != 0:
                        logger.warning('Restart vsftpd failed')
                        Display("- Restart vsftpd service failed...", "FAILED")
                        sys.exit(1)
                logger.info("set the restrict directories of ftp successfully")
                Display("- Set the restrict directories of ftp...", "FINISHED")

            elif not (chroot_check and chrootlist_check and listfile_check) :
                logger.info("set the restrict directories of ftp failed, wrong setting")
                Display("- Set the restrict directories of ftp...", "FAILED")
            else:
                logger.info("set the restrict directories of ftp failed, no set option")
                Display("- Set the restrict directories of ftp...", "FAILED")
        else:
            Display("- filepath /etc/vsftpd/vsftpd.conf not exist...", "SKIPPING")
    else:
        Display("- Skip set restrict directories of ftp due to config file...", "SKIPPING")
