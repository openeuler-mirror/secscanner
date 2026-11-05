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

def C03516_tcptimestamps():
    '''
    Function: Check whether the tcp_timestamps is disabled
    '''
    InsertSection("Check whether the tcp_timestamps is disabled")
    result = subprocess.run(['sysctl', 'net.ipv4.tcp_timestamps'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr[-1] != '0':
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03516\n")
        logger.warning("WRN_C03516: %s", WRN_C03516)
        logger.warning("SUG_C03516: %s", SUG_C03516)
        Display("- The tcp_timestamps is enabled...", "WARNING")
    else:
        logger.info("The tcp_timestamps is disabled")
        Display("- Check whether the tcp_timestamps is disabled...", "OK")
