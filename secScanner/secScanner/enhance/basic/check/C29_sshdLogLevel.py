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


def C29_sshdLogLevel():
    InsertSection("check the ssh loglevel")
    LOGLEVEL_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('LogLevel', line) and not re.match('^#|^$', line):
                LOGLEVEL_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'VERBOSE':
                    LOGLEVEL_SET = 'right'

    if LOGLEVEL_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC29\n")
        logger.warning("WRN_C29_01: %s", WRN_C29_01)
        logger.warning("SUG_C29: %s", SUG_C29)
        Display("- No ssh loglevel config set...", "WARNING")
    elif LOGLEVEL_SET == 'right':
        logger.info("Has ssh loglevel set, checking OK")
        Display("- Check the ssh loglevel...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC29\n")
        logger.warning("WRN_C29_02: %s", WRN_C29_02)
        logger.warning("SUG_C29: %s", SUG_C29)
        Display("- Wrong ssh loglevel config set...", "WARNING")
