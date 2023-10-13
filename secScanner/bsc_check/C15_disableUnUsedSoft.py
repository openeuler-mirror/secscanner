import logging
import os
import subprocess
from subprocess import PIPE
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def softck():
    resultServ = ''  # countServ dont need
    needStopSer = seconf.get('basic', 'unused_software_value').split()
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
                    for j in needStopSer:
                        if j == SERV_SOCK:
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
    if OS_ID.lower() in ['openEuler', 'bclinux']:
        if OS_DISTRO in ['7', '8', '22.03', '22.10', '22.10U1', '22.10U2', ]:
            softck()
        else:
            logger.warning(f"C15: Detected this system is {OS_ID}-{OS_DISTRO} , and not in os-distro ")
            Display("- No match items...", "WARNING")
    else:
        logger.warning(f"C15: This is unknown os-distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
