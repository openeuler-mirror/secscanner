# import utils
import subprocess
import shutil
import logging
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S14_sshRootDenie():
    InsertSection("set ssh root denie")
    DENY_ROOT_LOGIN = seconf.get('advance', 'deny_root_login')
    OS_DISTRO = get_value("OS_DISTRO")
    if DENY_ROOT_LOGIN == 'yes' or DENY_ROOT_LOGIN == 'YES':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        # ----------------Denie Telnet login---------------
        if OS_DISTRO == '7':
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

        # -----------------Denie Root ssh login----------------
        with open('/etc/ssh/sshd_config', 'r+') as f:
            lines = f.readlines()
            permitroot_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith("#PermitRootLogin"):
                    permitroot_exists = True
                    lines[i] = lines[i].replace("#", "")
                    if not re.search('no', line):
                        lines[i] = "PermitRootLogin no\n"
                    break
                elif line.strip().startswith("PermitRootLogin"):
                    permitroot_exists = True
                    if not re.search('no', line):
                        lines[i] = "PermitRootLogin no\n"
                    break
            if not permitroot_exists:
                lines.append("PermitRootLogin no\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()
        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('PermitRootLogin', line):
                    permitroot_exists = True
                    temp = line.split()
                    if temp[0] == 'PermitRootLogin' and temp[1] == 'no':
                        CHECK_EXIST = 1
        if not permitroot_exists:
            logger.info("No ssh Root Deny, setting failed")
            Display("- No ssh Root Denie set...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("Wrong ssh Root Deny, setting failed")
            Display("- Wrong ssh Root Denie set...", "FAILED")
        else:
            logger.info("Has ssh root deny set, setting ok")
            Display("- set the ssh root deny...", "FINISHED")
    else:
        Display("- Skip deny root login due to config file...", "SKIPPING")
