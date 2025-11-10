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

def C415_aideInstall():
    InsertSection("check if aide is installed")
    cmd_aide = "rpm -qa | grep  aide"
    ret, result = subprocess.getstatusoutput(cmd_aide)
    if ret == 0 and "aide" in result:
        logger.info("Has installed aide correctly, checking ok")
        Display("- Has installed aide correctly ...", "OK")
    elif ret == 1:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC415\n")
        logger.warning("WRN_C415: %s", WRN_C415)
        logger.warning("SUG_C415: %s", SUG_C415)
        Display("- Don't have aide installed...", "WARNING")
    else:
        logger.error("check the aide status failed")
        Display("- Error occured while checking aide status...", "FAILED")
