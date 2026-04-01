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

def C01_motd():
    InsertSection("check /etc/motd banner")
    if os.path.exists("/etc/motd") and os.path.getsize("/etc/motd"):
        logger.info("Has /etc/motd set, checking ok")
        Display("- Has /etc/motd set...",  "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01\n")
        logger.warning("WRN_C01: %s", WRN_C01)
        logger.warning("SUG_C01: %s", SUG_C01)
        Display("- No /etc/motd set...", "WARNING")
