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

def C0210_GIDunique():
    InsertSection("Check if GID is unique")
    if os.path.exists('/etc/group'):
        command = "cut -d: -f3 /etc/group | sort | uniq -d"
        ret, result = subprocess.getstatusoutput(command)
        if ret == 0 and result == '':
            logger.info("Confirm GID uniqueness, checking OK")
            Display("- Confirm GID uniqueness...", "OK")
        elif ret == 0 and result != '':
            result = result.strip().split('\n')
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0210\n")
            logger.warning("WRN_C0210_01: %s", WRN_C0210_01)
            logger.warning("SUG_C0210_01: %s", SUG_C0210_01)
            Display(f"- Duplicate GID {result}...", "WARNING")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0210\n")
            logger.warning("WRN_C0210_02: %s", WRN_C0210_02)
            logger.warning("SUG_C0210_02: %s", SUG_C0210_02)
            Display("- Failed to retrieve GID information...", "WARNING")
        
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0210\n")
        logger.warning("WRN_C0210_03: %s", WRN_C0210_03)
        logger.warning("SUG_C0210_03: %s", SUG_C0210_03)
        Display("- file /etc/group not exists...", "WARNING")
