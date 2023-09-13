import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S25_syslogFacility():
    SET_SSH_SYSLOGFACILITY = seconf.get('basic', 'set_ssh_syslogfacility')
    InsertSection("Set the syslogfacility...")
    if SET_SSH_SYSLOGFACILITY == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        # -----------------set the syslogfacility----------------
        with open('/etc/ssh/sshd_config', 'r+') as f:
            lines = f.readlines()
            facility_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith("#SyslogFacility"):
                    facility_exists = True
                    lines[i] = lines[i].replace("#", "")
                elif line.strip().startswith("SyslogFacility"):
                    facility_exists = True
                    if not re.search('AUTH', line):
                        lines[i] = "SyslogFacility AUTH\n"
                    break
            if not facility_exists:
                lines.append("SyslogFacility AUTH\n")
            f.seek(0)
            f.writelines(lines)
            f.truncate()

        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('SyslogFacility', line) and re.search('AUTH', line):
                    IS_EXIST = 1
                    temp = line.strip('\n').split()
                    if temp[0] == 'SyslogFacility' and temp[1] == 'AUTH':
                        CHECK_EXIST = 1
        if not facility_exists:
            logger.info("set the ssh syslogfacility failed, no set option")
            Display(f"- Set the ssh syslogfacility...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the ssh syslogfacility failed, wrong setting")
            Display(f"- Set the ssh syslogfacility...", "FAILED")
        else:
            logger.info("set the ssh syslogfacility successfully")
            Display(f"- Set the ssh syslogfacility...", "FINISHED")
    else:
        Display(f"- Skip set ssh syslogfacility due to config file...", "SKIPPING")
