# import utils
import subprocess
import shutil
import logging
from secScanner.lib import *
from secScanner.gconfig import *

def S14_sshRootDenie():
    logger = logging.getLogger("secscanner")
    InsertSection("set ssh root denie")
    DENY_ROOT_LOGIN = seconf.get('advance', 'deny_root_login')
    if DENY_ROOT_LOGIN == 'yes' or DENY_ROOT_LOGIN == 'YES':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        #----------------Denie Telnet login---------------
        if OS_DISTRO == '7' or OS_DISTRO == '6':
            if not os.path.exists('/etc/securetty_bak'):
                shutil.copy2('/etc/securetty', '/etc/securetty_bak')
            with open("/etc/securetty", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if not re.match('^#|^$', line) and "pts/" in line:
                        continue
                    file.write(line)
                file.truncate()
            with open("/etc/securetty", "r") as file:
                is_exist = sum(1 for line in file if not re.match('^#|^$', line) and "pts/" in line)

            if is_exist == 0:
                logger.info("Has telnet deny set, seting ok")
                Display("- set the telnet deny...", "FINISHED")
            else:
                logger.info("No ssh telnet Denie, seting failed")
                Display("- No Telnet Denie set...", "FAILED")

        #-----------------Denie Root ssh login----------------
        with open("/etc/ssh/sshd_config", "r+") as file:
            lines = file.readlines()
            file.seek(0)

            is_exist = sum(1 for line in lines if not re.match('^#|^$', line) and re.match('^PermitRootLogin', line))

            if is_exist > 0:
                for line in lines:
                    if re.match('^PermitRootLogin', line):
                        file.write("PermitRootLogin no\n")
                    else:
                        file.write(line)
                file.truncate()
            else:
                file.write("\nPermitRootLogin no\n")

        with open("/etc/ssh/sshd_config", "r") as file:
            is_exist = sum(1 for line in file if not re.match('^#|^$', line) and re.match('^PermitRootLogin', line))

            if is_exist == 0:
                logger.info("No ssh Root Deny, setting failed")
                Display("- No ssh Root Denie set...", "FAILED")
            else:
                if sum(1 for line in lines if not re.match('^#|^$', line) and re.match('^PermitRootLogin', line) and "no" in line) == 0:
                    logger.info("Wrong ssh Root Deny, setting failed")
                    Display("- Wrong ssh Root Denie set...", "FAILED")
                else:
                    logger.info("Has ssh root deny set, setting ok")
                    Display("- set the ssh root deny...", "FINISHED")

        logger.info("restart the sshd service...")
        subprocess.run(['systemctl', 'restart', 'sshd'])

    else:
        Display("- Skip deny root login due to config file...", "SKIPPING")
