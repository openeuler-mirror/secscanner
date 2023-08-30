import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil

def S29_sshLogLevel():
    SET_SSH_LOGLEVEL = seconf.get('basic', 'set_ssh_loglevel')
    logger = logging.getLogger("secscanner")
    InsertSection("Set the sshloglevel...")
    if SET_SSH_LOGLEVEL == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        # -----------------set the loglevel----------------
        IS_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('LogLevel', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\nLogLevel VERBOSE\n')
        else:
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.search('LogLevel', line):
                        write_file.write('LogLevel VERBOSE\n')
                    else:
                        write_file.write(line)
        IS_EXIST = 0
        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('LogLevel', line):
                    IS_EXIST = 1
                    temp = line.split()
                    if temp[0] == 'LogLevel' and temp[1] == 'VERBOSE':
                        CHECK_EXIST = 1
        if IS_EXIST == 0:
            logger.info("set the ssh loglevel failed,no set option")
            Display(f"- Set the ssh loglevel...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the ssh loglevel failed, wrong setting")
            Display(f"- Set the ssh loglevel...", "FAILED")
        else:
            logger.info("set the ssh loglevel successfully")
            Display(f"- Set the ssh loglevel...", "FINISHED")
    else:
        Display(f"- Skip set ssh loglevel due to config file...", "SKIPPING")
