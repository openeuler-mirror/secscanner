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
import os
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")

def C0232_targetSELinux():
    InsertSection("check SELinux policy")
    ret, result = subprocess.getstatusoutput("sestatus | grep 'Loaded policy name'")
    if ret == 0:
        result = result.split(':')[1].strip()
        if result == 'targeted':
            logger.info("SELinux policy configuration is correct, checking ok")
            Display("- check SELinux policy...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0232\n")
            logger.warning("WRN_C0232_01: %s", WRN_C0232_01)
            logger.warning("SUG_C0232_01: %s", SUG_C0232_01)
            Display("- Incorrect SELinux policy settings...", "WARNING")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0232\n")
        logger.warning("WRN_C0232_02: %s", WRN_C0232_02)
        logger.warning("SUG_C0232_02: %s", SUG_C0232_02)
        Display("- Failed to obtain SELinux policy...", "WARNING")
