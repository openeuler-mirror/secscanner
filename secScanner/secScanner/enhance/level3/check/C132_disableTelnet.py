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
logger = logging.getLogger("secscanner")

def C132_disableTelnet():
    InsertSection("Check if telnet is not enabled")
    ret, result = subprocess.getstatusoutput(f'netstat -tln | grep \':23\'')
    if ret != 0 and result == '':
        logger.info("Telnet not enabled...")
        Display("- Telnet not enabled...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC132\n")
        logger.warning("WRN_C132: %s", WRN_C132)
        logger.warning("SUG_C132: %s", SUG_C132)
        Display("- Telnet enabled...", "WARNING")

