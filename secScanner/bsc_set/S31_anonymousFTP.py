import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")

def S31_anonymousFTP():
    set_ftp_anonymous = seconf.get('advance', 'set_ftp_anonymous')
    InsertSection("Set the prohibit anonymous FTP...")
    if set_ftp_anonymous == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf') and not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
            shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
            # -----------------set the restrictFTPdir----------------
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            with open('/etc/vsftpd/vsftpd.conf', 'r+') as f:
                lines = f.readlines()
                anonymous_exists = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#anonymous_enable"):
                        anonymous_exists = True
                        lines[i] = lines[i].replace("#", "")
                    elif line.strip().startswith("anonymous_enable"):
                        anonymous_exists = True
                        if not re.search('NO', line):
                            lines[i] = "anonymous_enable=NO\n"
                        break
                if not anonymous_exists:
                    lines.append("anonymous_enable=NO\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            CHECK_EXIST = 0
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('anonymous_enable', line):
                        IS_EXIST = 1
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'anonymous_enable' and temp[1] == 'NO':
                            CHECK_EXIST = 1

            if not anonymous_exists:
                logger.info("set the prohibit anonymous FTP failed, no set option")
                Display(f"- Set the prohibit anonymous FTP...", "FAILED")
            elif CHECK_EXIST == 0:
                logger.info("set the prohibit anonymous FTP failed, wrong setting")
                Display(f"- Set the prohibit anonymous FTP...", "FAILED")
            else:
                result = subprocess.run(['systemctl', 'is-active', 'vsftpd'], stdout=subprocess.DEVNULL,
                                        stderr=subprocess.STDOUT)
                if result.returncode == 0:
                    subprocess.run(['systemctl', 'restart', 'vsftpd'])
                else:
                    subprocess.run(['systemctl', 'start', 'vsftpd'])
                logger.info("set the prohibit anonymous FTP successfully")
                Display(f"- Set the prohibit anonymous FTP...", "FINISHED")
        else:
            Display("- filepath /etc/vsftpd/vsftpd.conf not exist...", "SKIPPING")
    else:
        Display(f"- Skip set prohibit anonymous FTP due to config file...", "SKIPPING")
