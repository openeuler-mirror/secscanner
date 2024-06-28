import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S29_sshLogLevel():
    SET_SSH_LOGLEVEL = seconf.get('basic', 'set_ssh_loglevel')
    InsertSection("Set the ssh loglevel...")
    if SET_SSH_LOGLEVEL == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        add_bak_file('/etc/ssh/sshd_config_bak')
        # -----------------set the loglevel----------------
        with open('/etc/ssh/sshd_config', 'r+') as f:
            lines = f.readlines()
            loglevel_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith("#LogLevel"):
                    loglevel_exists = True
                    lines[i] = lines[i].replace("#", "")
                    if not re.search('VERBOSE', line):
                        lines[i] = "LogLevel VERBOSE\n"
                    break
                elif line.strip().startswith("LogLevel"):
                    loglevel_exists = True
                    if not re.search('VERBOSE', line):
                        lines[i] = "LogLevel VERBOSE\n"
                    break
            if not loglevel_exists:
                lines.append("LogLevel VERBOSE\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()
        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('LogLevel', line):
                    IS_EXIST = 1
                    temp = line.split()
                    if temp[0] == 'LogLevel' and temp[1] == 'VERBOSE':
                        CHECK_EXIST = 1
        if not loglevel_exists:
            logger.info("set the ssh loglevel failed,no set option")
            Display("- Set the ssh loglevel...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the ssh loglevel failed, wrong setting")
            Display("- Set the ssh loglevel...", "FAILED")
        else:
            logger.info("set the ssh loglevel successfully")
            Display("- Set the ssh loglevel...", "FINISHED")
    else:
        Display("- Skip set ssh loglevel due to config file...", "SKIPPING")
