import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
import subprocess
logger = logging.getLogger("secscanner")


def S13_restrictFTPdir():
    set_ftp_restrictdir = seconf.get('basic', 'set_ftp_restrictdir')
    InsertSection("Set the restrictFTPdir...")
    if set_ftp_restrictdir == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf') and not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
            shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
            # -----------------set the restrictFTPdir----------------
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            with open('/etc/vsftpd/vsftpd.conf', 'r+') as f:
                lines = f.readlines()
                chroot_exists = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#chroot_local_user"):
                        chroot_exists = True
                        lines[i] = lines[i].replace("#", "")
                    elif line.strip().startswith("chroot_local_user"):
                        chroot_exists = True
                        if not re.search('YES', line):
                            lines[i] = "chroot_local_user=YES\n"
                        break
                if not chroot_exists:
                    lines.append("chroot_local_user=YES\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            CHECK_EXIST = 0
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('chroot_local_user', line):
                        IS_EXIST = 1
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'chroot_local_user' and temp[1] == 'YES':
                            CHECK_EXIST = 1

            if not chroot_exists:
                logger.info("set the ssh restrictFTPdir failed, no set option")
                Display(f"- Set the ssh restrictFTPdir...", "FAILED")
            elif CHECK_EXIST == 0:
                logger.info("set the ssh restrictFTPdir failed, wrong setting")
                Display(f"- Set the ssh restrictFTPdir...", "FAILED")
            else:
                result = subprocess.run(['systemctl', 'is-active', 'vsftpd'], stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)
                if result.returncode == 0:
                    subprocess.run(['systemctl', 'restart', 'vsftpd'])
                else:
                    subprocess.run(['systemctl', 'start', 'vsftpd'])
                logger.info("set the ssh restrictFTPdir successfully")
                Display(f"- Set the ssh restrictFTPdir...", "FINISHED")
        else:
            Display("- filepath /etc/vsftpd/vsftpd.conf not exist...", "SKIPPING")
    else:
        Display(f"- Skip set ssh restrictFTPdir due to config file...", "SKIPPING")