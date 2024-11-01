import logging
import os
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *

logger = logging.getLogger("secscanner")


def softck():
    resultServ = ''  # countServ dont need
    needStopSer = seconf.get('basic', 'unused_software_value').split()
    ret, result = subprocess.getstatusoutput(f'systemctl list-units')
    if ret ==0:
        result = result.split('\n')

    if len(result) > 0:
        for line in result:
            if line:
                serv_sock = line.split()[0]
                if ('.service' in serv_sock) or ('.socket' in serv_sock):
                    for j in needStopSer:
                        if j == serv_sock:
                            resultServ += j + ' '

    if len(resultServ) > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC15\n")
        logger.warning("WRN_C15_01: %s", WRN_C15_01)
        logger.warning("SUG_C15: %s", SUG_C15)
        Display(f"- Service {resultServ} need stop...", "WARNING")
    else:
        logger.warning("WRN_C15_02: %s", WRN_C15_02)
        logger.warning("SUG_C15: %s", SUG_C15)
        Display("- No service need stop...", "OK")


def C15_disableUnUsedSoft():
    InsertSection("check the unused software")
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    if OS_ID.lower() in ['openeuler', 'bclinux']:
        if OS_DISTRO in ['7', '8', '22.03', '22.10', '22.10U1', '22.10U2', 'v24', '24', '21.10U4']:
            softck()
        else:
            logger.warning(f"C15: Detected this system is {OS_ID}-{OS_DISTRO} , and not in os-distro ")
            Display("- No match items...", "WARNING")
    else:
        logger.warning(f"C15: This is unknown os-distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
