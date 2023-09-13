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
    SHELL_RUN = subprocess.run(['systemctl', 'list-units', '--type=service', '--type=socket'], stdout=PIPE)
    SHELL_RESULT = SHELL_RUN.stdout  # get shell result, SHELL_RESULT is a stream of bytes
    temp = SHELL_RESULT.split(b'\n', -1)  # cut the byte stream by lines
    for i in range(len(temp)):
        line_list = temp[i].decode().split()  # delete space and split
        if len(line_list) > 3 and line_list[1] == 'loaded' and line_list[2] != 'failed' and line_list[3] != 'exited':
            # make sure service or socket is 'loaded', cant be failed, cant be exited
            SERV_SOCK = line_list[0]
            if ('.service' in SERV_SOCK) or ('.socket' in SERV_SOCK):
                for j in needStopSer:  # find if there is a needstopser in string(.service or .socket)
                    if j in SERV_SOCK:
                        resultServ = resultServ + j + ' '  # save results in a string

    if len(resultServ) > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC15\n")
        logger.warning("WRN_C15: %s", WRN_C05)
        logger.warning("SUG_C15: %s", SUG_C15)
        Display(f"- Service {resultServ} need stop...", "WARNING")
    else:
        logger.info("No service need to stop, checking ok")
        Display("- No service need stop...", "OK")


def C15_disableUnUsedSoft():
    InsertSection("check the unused software")
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    if OS_ID.lower() in ['openEuler', 'bclinux']:
        if OS_DISTRO in ['7', '8', '22.03', '22.10', '22.10U1', '22.10U2', ]:
            softck()
        else:
            logger.warning(f"WRN_C15_01: Detected this system is {OS_ID}-{OS_DISTRO} , and not in os-distro ")
            Display("- No match items...", "WARNING")
    else:
        logger.warning(f"WRN_C15_02: This is unknown os-distro, we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
