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

def C0303_startFirewalld():
    InsertSection("Check if firewalld is launched")
    ret1, result1 = subprocess.getstatusoutput("systemctl is-active firewalld")
    ret2, result2 = subprocess.getstatusoutput("systemctl is-active iptables")
    ret3, result3 = subprocess.getstatusoutput("systemctl is-active nftables")
    if ret1 == 0 and result1 == "active" and ret2 == 3 and result2 == "inactive" and ret3 == 3 and result3 == "inactive":
        logger.info("Checking Firewalld is active and iptables&nftables is inactive")
        Display("- Checking Firewalld is active", "OK")
    elif ret1 == 0 and result1 == "active":
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0303\n")
        logger.warning("WRN_C0303_01: %s", WRN_C0303_01)
        logger.warning("SUG_C0303_01: %s", SUG_C0303_01)
        Display("- Checking Firewalld is active, iptables or nftables actice too...", "WARNING")
    elif ret1 == 3 and result1 == "inactive":
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0303\n")
        logger.warning("WRN_C0303_02: %s", WRN_C0303_02)
        logger.warning("SUG_C0303_02: %s", SUG_C0303_02)
        Display("- Checking Firewalld is inactive(dead)...", "WARNING")
    else:
        logger.error("Unexpected error while checking firewalld status")
        Display("- Unexpected error while checking firewalld status...", "FAILED")