import os
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")

disable_unused_software = seconf.get('basic', 'disable_unused_software')
unused_software_value = seconf.get('basic', 'unused_software_value').split()

def dis():
    ret, result = subprocess.getstatusoutput(f'systemctl list-units')
    if ret ==0:
        out = result.split('\n')

    if len(out) > 0:
        for line in out:
            if line:
                serv_sock = line.split()[0]
                if ('.service' in serv_sock) or ('.socket' in serv_sock):
                    for j in unused_software_value:
                        if j == serv_sock:
                            flag, res =  subprocess.getstatusoutput(f'systemctl stop {j}')
                            if flag !=0:
                                logger.warning(f"Stop the unused software: {j} fail")

                            logger.info(f"Stop the unused software: {j}, you can use systemctl start {j} to start it...")

                            en, serv_en = subprocess.getstatusoutput(f'systemctl is-enabled {j}')
                            if en !=0:
                                logger.warning(f"Check the unused software: {j} is enabled fail")
                                
                            else:
                                if serv_en == 'enabled':
                                    dis, serv_dis = subprocess.getstatusoutput(f'systemctl disable {j}')
                                    if dis !=0:
                                        logger.warning(f"Disable the unused software: {j} fail")
                                        
                                    logger.info(f"Disable the unused software: {j}, you can use systemctl enable {j} to enable it...")

def S15_disableUnUsed():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("Disable the UnUsed software")
    if disable_unused_software == 'yes':
        if OS_ID.lower() in ['bclinux', 'openeuler']:
            if OS_DISTRO in ['7', '8', '21.10', '22.10', '22.10U1', '22.10U2', 'v24', '24']:
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
