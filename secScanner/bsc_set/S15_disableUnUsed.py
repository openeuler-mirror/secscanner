import os
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")

DISABLE_UNUSED_SOFTWARE = seconf.get('basic', 'disable_unused_software')
UNUSED_SOFTWARE_VALUE = seconf.get('basic', 'unused_software_value').split()

def dis():
    command1 = ['systemctl', '-l']
    command2 = ['grep', 'running']
    output1 = subprocess.run(command1, stdout=subprocess.PIPE)
    output2 = subprocess.run(command2, input=output1.stdout, stdout=subprocess.PIPE)
    result = output2.stdout.decode().split('\n')
    if len(result) > 0:
        for line in result:
            if line:
                SERV_SOCK = line.split()[0]
                if ('.service' in SERV_SOCK) or ('.socket' in SERV_SOCK):
                    for j in UNUSED_SOFTWARE_VALUE:
                        if j == SERV_SOCK:
                            subprocess.run(['systemctl', 'stop', j])
                            logger.info(f"Stop the unused software: {j}, you can use systemctl start {j} to enable it...")

                            enable_ser = subprocess.run(['systemctl', 'is-enabled', j], stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE)
                            run_out = len(enable_ser.stdout)
                            run_err = len(enable_ser.stderr)
                            if RUN_ERR == 0 and RUN_OUT != 0:
                                subprocess.run(['systemctl', 'disable', j])
                                logger.info(f"Disable the unused software: {j}, you can use systemctl enable {j} to enable it...")


def S15_disableUnUsed():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("Disable the UnUsed software")
    if DISABLE_UNUSED_SOFTWARE == 'yes':
        if OS_ID.lower() in ['bclinux', 'openEuler']:
            if OS_DISTRO in ['7', '8', '21.10', '22.10', '8', '22.10U1', '22.10U2', 'v24']:
                dis()
                logger.info("This is RHEL system, disable the unused software...")
                Display(f"- Disable the {OS_ID}-{OS_DISTRO} unused software...", "FINISHED")
            else:
                logger.info(f"We do not support {OS_ID}-{OS_DISTRO} at this moment")
                Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
        else:
            logger.info(f"This is not RHEL Distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")

    else:
        Display("- Skip disable unused software due to config file...", "SKIPPING")
