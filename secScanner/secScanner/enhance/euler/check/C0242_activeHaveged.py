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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0242_activeHaveged():
    InsertSection("Check if the haveged service is running")
    ret, result = subprocess.getstatusoutput('rpm -qa haveged')
    if ret == 0 and result != '':
        out, output = subprocess.getstatusoutput('systemctl is-active haveged')
        if out == 0 and output == 'active':
            logger.info("service haveged already active, checking ok")
            Display("- service haveged already active...", "OK")
        elif output == 'inactive':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0242\n")
            logger.warning("WRN_C0242_01: %s", WRN_C0242_01)
            logger.warning("SUG_C0242_01: %s", SUG_C0242_01)
            Display("- Haveged service inactive...", "WARNING")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0242\n")
            logger.warning("WRN_C0242_02: %s", WRN_C0242_02)
            logger.warning("SUG_C0242_01: %s", SUG_C0242_01)
            Display("- Failed to obtain the active status of the active state...", "WARNING")
    elif ret == 0 and result == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0242\n")
        logger.warning("WRN_C0242_03: %s", WRN_C0242_03)
        logger.warning("SUG_C0242_02: %s", SUG_C0242_02)
        Display("- Haveged not installed...", "WARNING")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0242\n")
        logger.warning("WRN_C0242_04: %s", WRN_C0242_04)
        logger.warning("SUG_C0242_02: %s", SUG_C0242_02)
        Display("- Failed to obtain the installation status of haveged...", "WARNING")
