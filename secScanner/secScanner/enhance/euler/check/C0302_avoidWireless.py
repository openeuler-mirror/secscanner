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

def C0302_avoidWireless():
    InsertSection("Check avoid using wireless network")
    ret1, result1 = subprocess.getstatusoutput("nmcli radio all")
    if ret1 == 0:
        lines = result1.split("\n")
        status = lines[1].strip().split()
        if status[1].strip() in ["disabled", "已禁用"] and status[3].strip() in ["disabled", "已禁用"]:
            logger.info("Checking wireless network is disabled")
            Display("- Checking wireless network is disabled", "OK")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0302\n")
            logger.warning("WRN_C0302: %s", WRN_C0302)
            logger.warning("SUG_C0302: %s", SUG_C0302)
            Display("- Wireless network should be banned...", "WARNING")
    else:
        logger.warning("Excute cmd: 'nmcli radio all' failed")
        Display("- A error occurred while checking nmcli raido...", "WARNING")
