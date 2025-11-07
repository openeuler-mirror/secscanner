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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0228_warnBanner():
    InsertSection("check system warning  banner")
    if os.path.exists("/etc/motd") and os.path.getsize("/etc/motd"):
        logger.info("Has /etc/motd set, checking ok")
        Display("- Has /etc/motd warning banner...",  "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0228\n")
        logger.warning("WRN_C0228_01: %s", WRN_C0228_01)
        logger.warning("SUG_C0228_01: %s", SUG_C0228_01)
        Display("- No /etc/motd set...", "WARNING")

    if os.path.exists("/etc/issue") and os.path.getsize("/etc/issue"):
        logger.info("Has /etc/issue set, checking ok")
        Display("- Has /etc/issue warning banner...",  "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0228\n")
        logger.warning("WRN_C0228_02: %s", WRN_C0228_02)
        logger.warning("SUG_C0228_02: %s", SUG_C0228_02)
        Display("- No /etc/issue set...", "WARNING")

    if os.path.exists("/etc/issue.net") and os.path.getsize("/etc/issue.net"):
        logger.info("Has /etc/issue.net set, checking ok")
        Display("- Has /etc/issue.net warning banner...",  "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0228\n")
        logger.warning("WRN_C0228_03: %s", WRN_C0228_03)
        logger.warning("SUG_C0228_03: %s", SUG_C0228_03)
        Display("- No /etc/issue.net set...", "WARNING")

