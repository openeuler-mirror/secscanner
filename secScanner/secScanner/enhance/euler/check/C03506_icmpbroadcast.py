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

def C03506_icmpbroadcast():
    '''
    Function: Check whether the system does not respond ICMP broadcast packets
    '''
    InsertSection("Check whether the system does not respond ICMP broadcast packets")
    result = subprocess.run(['sysctl', 'net.ipv4.icmp_echo_ignore_broadcasts'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr[-1] != '1':
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03506\n")
        logger.warning("WRN_C03506: %s", WRN_C03506)
        logger.warning("SUG_C03506: %s", SUG_C03506)
        Display("- The system responds to ICMP broadcast packets...", "WARNING")
    else:
        logger.info("The system does not respond to ICMP broadcast packets")
        Display("- Check whether the system does not respond ICMP broadcast packets...", "OK")
