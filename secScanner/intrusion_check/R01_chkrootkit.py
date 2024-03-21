import logging
import subprocess
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def check_rootkit():
    InsertSection("using chkrootkit check the system rootkit")
    ret, result = subprocess.getstatusoutput('rpm -qa')
    if ret !=0:
        logger.warning("'rpm -qa' command execution failed")
    temp = result.split('\n', -1)  # cut the byte stream by lines
    is_exist = 0
    command_path = '/opt/secScanner/secScanner/.commands/'
    for i in range(len(temp)):
        line = temp[i]
        if 'chkrootkit' in line:
            is_exist = 1
    if is_exist == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nR01\n")
        logger.info("the system doesn't install chkrootkit, please install it ...")
        Display("- No chkrootkit install...", "WARNING")
    else:
        if not os.path.exists(command_path):
            os.mkdir(command_path)
        cmd = 'which --skip-alias awk cut echo find egrep id head ls netstat ps strings sed uname'
        ret, result = subprocess.getstatusoutput(cmd)
        if ret != 0:
            logger.warning(f'{cmd} command execution failed')
            Display(f"- {cmd} command execution failed...", "WARNING")
            sys.exit(1)
        result = result.split("\n")
        for i in result:
            if not i:
                continue
            ret, result = subprocess.getstatusoutput(f'cp -p {i} {command_path}')
            if ret != 0:
                logger.warning('CP command execution failed')
                Display("- CP command execution failed...", "WARNING")
                sys.exit(1)
        ret, result = subprocess.getstatusoutput('`which chkrootkit`')
        if ret != 0:
            logger.warning('chkrootkit command execution failed')
            Display("- chkrootkit command execution failed...", "WARNING")
            sys.exit(1)
        with open(LOGFILE, "a") as file:
            file.write(f"{result}\n")
        count = 0
        with open(LOGFILE, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.search('INFECTED', line):
                    count = count + 1
        if count > 0:
            logger.info("ROOTKIT_R01: %s", ROOTKIT_R01)
            logger.warning("Suggestion: %s", SUG_R01)
            Display("- the system might be infected...", "WARNING")
        else:
            Display("- Checking rootkit finished...", "OK")


def R01_chkrootkit():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    if OS_ID.lower() in ['centos', 'rhel', 'redhat', 'bclinux', 'openeuler']:
        if OS_DISTRO in ['7', '8', '21.10', '22.10', '22.10U1', '22.10U2', '22.03', 'v24', '24']:
            check_rootkit()
        else:
            logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.info(f"This is not RHEL Distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
