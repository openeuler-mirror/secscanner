import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
def S13_sshProtocol():
    logger = logging.getLogger("secscanner")
    SET_SSH_PROTOCOL = seconf.get('basic', 'set_ssh_protocol')
    InsertSection("Set ssh Protocol...")
    if SET_SSH_PROTOCOL == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        IS_EXIST = 0

        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line) and re.search('Protocol', line)):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\nProtocol 2\n')
        else:
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.match('Protocol', line):
                        write_file.write("Protocol 2\n")
                    else:
                        write_file.write(line)

        IS_EXIST = 0
        PROTOCOL_RESULT = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line) and re.search('Protocol', line)):
                    IS_EXIST = 1
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1].isdigit():
                        PROTOCOL_RESULT = 1
        if IS_EXIST == 0:
            logger.info("No ssh protocol set, set failed")
            Display(f"- No ssh protocol config set...", "FAILED")
        else:
            if PROTOCOL_RESULT == 0:
                logger.info("Wrong ssh protocol set, checking failed")
                Display(f"- Wrong ssh protocol config set...", "FAILED")
            else:
                logger.info("set the ssh protocol, checking ok")
                Display(f"- Set the ssh protocol...", "FINISHED")
    else:
        Display(f"- Skip set ssh protocol due to config file...", "SKIPPING")