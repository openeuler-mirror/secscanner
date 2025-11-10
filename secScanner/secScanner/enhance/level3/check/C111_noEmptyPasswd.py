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

def C111_noEmptyPasswd():
    InsertSection("check prohibit users with empty passwords")
    if os.path.exists('/etc/shadow'):
        command = "awk -F: '($2 == \"\") { exit 1 }' /etc/shadow"
        ret, result = subprocess.getstatusoutput(command)
        if ret == 1:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC111\n")
            logger.warning("WRN_C111_01: %s", WRN_C111_01)
            logger.warning("SUG_C111_01: %s", SUG_C111_01)
            Display("- There is an empty password user present...", "WARNING")
        else:
            logger.info("Has no empty password user, checking OK")
            Display("- Check no empty password user...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC111\n")
        logger.warning("WRN_C111_02: %s", WRN_C111_02)
        logger.warning("SUG_C111_02: %s", SUG_C111_02)
        Display("- file /etc/shadow does not exist...", "WARNING")

