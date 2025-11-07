# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, 
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, 
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''


import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0301_uncommonNetwork():
    InsertSection("Check avoid using uncommon network service")
    ret1, result1 = subprocess.getstatusoutput("modprobe -n -v sctp")
    ret2, result2 = subprocess.getstatusoutput("modprobe -n -v tipc")
    sctp_flag = False
    tipc_flag = False
    if "install /bin/true" in result1:
        sctp_flag = True
    elif "not found in directory" in result1:
        sctp_flag = True
    elif "insmod /lib/modules/" in result1:
        sctp_flag = False
    else:
        logger.warning("A error occurred while checking sctp")
        Display("- A error occurred while checking sctp...", "WARNING")
        return
    if "install /bin/true" in result2:
        tipc_flag = True
    elif "not found in directory" in result2:
        tipc_flag = True
    elif "insmod /lib/modules/" in result2:
        tipc_flag = False
    else:
        logger.warning("A error occurred while checking tipc")
        Display("- A error occurred while checking tipc...", "WARNING")
        return
    # display checking result
    if sctp_flag and tipc_flag:
        Display("- Avoid using uncommon network service...", "OK")
    elif not sctp_flag and not tipc_flag:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0301\n")
        logger.warning("WRN_C0301_01: %s", WRN_C0301_01)
        logger.warning("SUG_C0301_01: %s", SUG_C0301_01)
        Display("- Check sctp and tipc should be avoided...", "WARNING")
    elif sctp_flag and not tipc_flag:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0301\n")
        logger.warning("WRN_C0301_02: %s", WRN_C0301_02)
        logger.warning("SUG_C0301_02: %s", SUG_C0301_02)
        Display("- Check tipc should be avoided...", "WARNING")
    elif not sctp_flag and tipc_flag:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0301\n")
        logger.warning("WRN_C0301_03: %s", WRN_C0301_03)
        logger.warning("SUG_C0301_03: %s", SUG_C0301_03)
        Display("- Check sctp should be avoided...", "WARNING")
