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

def C0204_rootUIDunique():
    InsertSection("Check if root UID is unique")
    if os.path.exists('/etc/passwd'):
        command = "awk -F: '($3 == 0) { print $1 }' /etc/passwd"
        ret, result = subprocess.getstatusoutput(command)
        if ret == 0:
            result = result.strip()
            if result == 'root':
                logger.info("check root UID unique, checking ok")
                Display("- check root UID unique ...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0204\n")
                logger.warning("WRN_C0204_01: %s", WRN_C0204_01)
                logger.warning("SUG_C0204_01: %s", SUG_C0204_01)
                Display("- There are users with UID 0 who are not root ...", "WARNING")

        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0204\n")
            logger.warning("WRN_C0204_02: %s", WRN_C0204_02)
            logger.warning("SUG_C0204_02: %s", SUG_C0204_02)
            Display("- Failed to obtain information with UID 0 ...", "WARNING")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0204\n")
        logger.warning("WRN_C0204_03: %s", WRN_C0204_03)
        logger.warning("SUG_C0204_03: %s", SUG_C0204_03)
        Display("- file /etc/passwd does not exist...", "WARNING")

