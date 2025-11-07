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


import os
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")


def C133_removehttp():
    InsertSection("Check if software HTTP exists")
    ret, result = subprocess.getstatusoutput('rpm -qa httpd*')
    if ret == 0 and result.strip():
        with open(RESULT_FILE, "a") as file:
            file.write("\nC133\n")
        logger.warning("WRN_C133_01: %s", WRN_C133_01)
        logger.warning("SUG_C133_01: %s", SUG_C133_01)
        Display("- HTTP not removed...", "WARNING")
    elif ret == 0 and not result.strip():
        logger.info("Http not installed, checking ok...")
        Display("- check http not installed...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC133\n")
        logger.warning("WRN_C133_02: %s", WRN_C133_02)
        logger.warning("SUG_C133_02: %s", SUG_C133_02)
        Display("- Query command execution failed...", "WARNING")

