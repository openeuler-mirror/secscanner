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

def C113_GIDunique():
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
                file.write("\nC113\n")
            logger.warning("WRN_C113_01: %s", WRN_C113_01)
            logger.warning("SUG_C113_01: %s", SUG_C113_01)
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC113\n")
            logger.warning("WRN_C113_02: %s", WRN_C113_02)
            logger.warning("SUG_C113_02: %s", SUG_C113_02)
            Display("- Failed to retrieve GID information...", "WARNING")
        
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC113\n")
        logger.warning("WRN_C113_03: %s", WRN_C113_03)
        logger.warning("SUG_C113_03: %s", SUG_C113_03)
        Display("- file /etc/group not exists...", "WARNING")
