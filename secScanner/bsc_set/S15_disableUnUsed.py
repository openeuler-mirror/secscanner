import os
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")
DISABLE_UNUSED_SOFTWARE = seconf.get('basic', 'disable_unused_software')
UNUSED_SOFTWARE_VALUE = seconf.get('basic', 'unused_software_value').split()

def rhel78_dis():
    SHELL_RUN = subprocess.run(['systemctl', 'list-units', '--type=service', '--type=socket'], stdout=subprocess.PIPE)
    SHELL_RESULT = SHELL_RUN.stdout  # get shell result, SHELL_RESULT is a stream of bytes
    temp = SHELL_RESULT.split(b'\n', -1)  # cut the byte stream by lines
    for i in range(len(temp)):
        line_list = temp[i].decode().split()#delete space and split
        if len(line_list) > 3 and line_list[1] == 'loaded' and line_list[2] != 'failed' and line_list[3] != 'exited':
            # make sure service or socket is 'loaded', cant be failed, cant be exited
            SERV_SOCK = line_list[0]
            if ('.service' in SERV_SOCK) or ('.socket' in SERV_SOCK):
                for j in UNUSED_SOFTWARE_VALUE:# find if there is a needstopser in string(.service or .socket)
                    if j in SERV_SOCK:
                        SYSTEMCTL_RUN = subprocess.run(['systemctl', 'is-active', j], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                        RUN_OUT = len(SYSTEMCTL_RUN.stdout)
                        RUN_ERR = len(SYSTEMCTL_RUN.stderr)
                        if RUN_ERR == 0 and RUN_OUT != 0:
                            print(f"stop {j}")
                            subprocess.run(['systemctl', 'stop', j])
                            logger.info(f"Stop the unused software: {j}, you can use systemctl start {j} to enable it...")

                        SYSTEMCTL_RUN = subprocess.run(['systemctl', 'is-enabled', j], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        RUN_OUT = len(SYSTEMCTL_RUN.stdout)
                        RUN_ERR = len(SYSTEMCTL_RUN.stderr)
                        if RUN_ERR == 0 and RUN_OUT != 0:
                            print(f"diable {j}")
                            subprocess.run(['systemctl', 'disable', j])
                            logger.info(f"Disable the unused software: {j}, you can use systemctl enable {j} to enable it...")
def rhel6_dis():
    for i in UNUSED_SOFTWARE_VALUE:
        if os.path.exists(f"/etc/init.d/{i}"):
            subprocess.run(['chkconfig', i, 'off'])
            subprocess.run(['service', i, 'stop'])
            logger.info(f"Disable the unused software: {i}, you can use chkconfig {i} on to enable it...")

def S15_disableUnUsed():
    InsertSection("Disable the UnUsed software")
    if DISABLE_UNUSED_SOFTWARE == 'yes':
        if OS_ID.lower() in ['centos', 'rehl', 'redhat', 'bclinux', '\"centos\"', '\"rehl\"', '\"redhat\"', '\"bclinux\"']:
            if OS_DISTRO in ['7', '8', '\"7\"', '\"8\"']:
                rhel78_dis()
                logger.info("This is RHEL system, disable the unused software...")
                Display(f"- Disable the {OS_ID}-{OS_DISTRO} unused software...", "FINISHED")
            elif OS_DISTRO in ['6', '\"6\"']:
                rhel6_dis()
                logger.info("This is RHEL6 system, disable the unused software...")
                Display(
                    f"- Disable the {OS_ID}-{OS_DISTRO} unused software...", "FINISHED")
            else:
                logger.info(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
                Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
        else:
            logger.info(f"This is not RHEL Distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")

    else:
        Display(f"- Skip disable unused software due to config file...", "SKIPPING")
