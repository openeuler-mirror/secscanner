import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
import pathlib
logger = logging.getLogger("secscanner")

def S30_ftpBanner():
    InsertSection("Set the ftp banner...")
    set_ftp_banner = seconf.get('advance', 'set_ftp_banner')
    if set_ftp_banner == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf') and not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
            shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            with open('/etc/vsftpd/vsftpd.conf', 'r+') as f:
                lines = f.readlines()
                found_banner = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#ftpd_banner"):
                        lines[i] = line.replace("#", "")
                        if not re.search('Authorized', line):
                            lines[i] = "ftpd_banner=Authorized users only. All activity may be monitored and reported.\n"
                        found_banner = True
                        break
                    elif line.strip().startswith("ftpd_banner"):
                        if not re.search('Authorized', line):
                            lines[i] = "ftpd_banner=Authorized users only. All activity may be monitored and reported.\n"
                        found_banner = True
                        break
                if not found_banner:
                    lines.append("ftpd_banner=Authorized users only. All activity may be monitored and reported.\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            CHECK_EXIST = 0
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('ftpd_banner', line):
                        IS_EXIST = 1
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'ftpd_banner' and temp[1] == ('Authorized users only. All activity may be '
                                                                    'monitored and reported.'):
                            CHECK_EXIST = 1

            if not found_banner:
                logger.info("set the ftp banner failed, no set option")
                Display("- Set the ftp banner...", "FAILED")
            elif CHECK_EXIST == 0:
                logger.info("set the ftp banner failed, wrong setting")
                Display("- Set the ftp banner...", "FAILED")
            else:
                ret, result = subprocess.getstatusoutput('systemctl is-active vsftpd')
                if ret != 0:
                    flag, out = subprocess.getstatusoutput('systemctl start vsftpd')
                    if flag != 0:
                        logger.warning('Start vsftpd failed')
                        Display("- Start vsftpd service failed...", "FAILED")
                        return
                else:
                    flag, out = subprocess.getstatusoutput('systemctl restart vsftpd')
                    if flag != 0:
                        logger.warning('Restart vsftpd failed')
                        Display("- Restart vsftpd service failed...", "FAILED")
                        return
                logger.info("set the ftp banner successfully")
                Display("- Set the ftp banner...", "FINISHED")
        else:
            Display("- filepath /etc/vsftpd/vsftpd.conf not exist...", "SKIPPING")
    else:
        Display("- Skip set ftp banner due to config file...", "SKIPPING")
