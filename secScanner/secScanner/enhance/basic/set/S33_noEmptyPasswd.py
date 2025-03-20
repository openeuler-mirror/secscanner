import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S33_noEmptyPasswd():
    set_ssh_permitemptypasswd = seconf.get('basic', 'set_ssh_permitemptypasswd')
    InsertSection("Set the ssh permitemptypasswd...")
    if set_ssh_permitemptypasswd == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        add_bak_file('/etc/ssh/sshd_config_bak')
        # -----------------set the permitemptypasswd----------------
        with open('/etc/ssh/sshd_config', 'r+') as f:
            lines = f.readlines()
            config_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith("#PermitEmptyPasswords"):
                    config_exists = True
                    lines[i] = lines[i].replace("#", "")
                    if not re.search('no', line):
                        lines[i] = "PermitEmptyPasswords no\n"
                    break
                elif line.strip().startswith("PermitEmptyPasswords"):
                    config_exists = True
                    if not re.search('no', line):
                        lines[i] = "PermitEmptyPasswords no\n"
                    break
            if not config_exists:
                lines.append("PermitEmptyPasswords no\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()
        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('PermitEmptyPasswords', line):
                    temp = line.split()
                    if temp[0] == 'PermitEmptyPasswords' and temp[1] == 'no':
                        CHECK_EXIST = 1
        if not config_exists:
            logger.info("set the ssh PermitEmptyPasswords failed,no set option")
            Display("- Set the ssh PermitEmptyPasswords...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the ssh PermitEmptyPasswords failed, wrong setting")
            Display("- Set the ssh PermitEmptyPasswords...", "FAILED")
        else:
            logger.info("set the ssh PermitEmptyPasswords successfully")
            Display("- Set the ssh PermitEmptyPasswords...", "FINISHED")
    else:
        Display("- Skip set ssh PermitEmptyPasswords due to config file...", "SKIPPING")
