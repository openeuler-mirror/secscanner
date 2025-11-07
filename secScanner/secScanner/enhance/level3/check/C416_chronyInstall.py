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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C416_chronyInstall():
    InsertSection("check if chrony is installed")
    cmd_chrony = "rpm -qa | grep chrony"
    ret, result = subprocess.getstatusoutput(cmd_chrony)
    if ret == 0 and "chrony" in result:
        logger.info("Has installed chrony correctly, checking ok")
        Display("- Has installed chrony correctly ...", "OK")

    elif ret == 1 :
        with open(RESULT_FILE, "a") as file:
            file.write("\nC416\n")
        logger.warning("WRN_C416: %s", WRN_C416)
        logger.warning("SUG_C416: %s", SUG_C416)
        Display("- Don't have chrony installed...", "WARNING")
    else:
        logger.error("check the chrony status failed")
        Display("- Error occured while checking chrony status...", "FAILED")
