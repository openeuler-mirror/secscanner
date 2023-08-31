import logging
import subprocess
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")
def check_rootkit():
    InsertSection("using chkrootkit check the system rootkit")
    SHELL_RUN = subprocess.run(['rpm', '-qa'], stdout=subprocess.PIPE)
    SHELL_RESULT = SHELL_RUN.stdout  # get shell result, SHELL_RESULT is a stream of bytes
    temp = SHELL_RESULT.split(b'\n', -1)  # cut the byte stream by lines
    IS_EXIST = 0
    for i in range(len(temp)):
        line = temp[i].decode()
        if 'chkrootkit' in line:
            IS_EXIST = 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nR01\n")
        logger.info("the system doesn't install chkrootkit, please install it ...")
        Display("- No chkrootkit install...", "WARNING")
    else:
        if not os.path.exists("/opt/BCLinux/bse/.commands"):
            os.mkdir("/opt/BCLinux/bse/.commands")
        SHELL_RUN = subprocess.run(['which', '--skip-alias', 'awk', 'cut', 'echo', 'find', 'egrep', 'id', 'head',
                                    'ls', 'netstat', 'ps', 'strings', 'sed', 'uname'], stdout=subprocess.PIPE)
        SHELL_RESULT = SHELL_RUN.stdout.decode().split("\n")
        for i in SHELL_RESULT:
            subprocess.run(['cp', i, '/opt/BCLinux/bse/.commands'])
        SHELL_RUN = subprocess.run(['chkrootkit'], stdout=subprocess.PIPE)
        SHELL_RESULT = SHELL_RUN.stdout.decode()
        with open(LOGFILE, "a") as file:
            file.write(f"{SHELL_RESULT}\n")
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
    if OS_ID.lower() in ["centos", "\"centos\"", "rhel", "\"rhel\"", "redhat", "\"redhat\"", "bclinux", "\"bclinux\""]:
        if OS_DISTRO in ["8", "7", "\"8\"", "\"7\""]:
            check_rootkit()
        else:
            logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.info(f"This is not RHEL Distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
