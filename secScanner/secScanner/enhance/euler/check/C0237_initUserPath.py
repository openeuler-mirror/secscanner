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


def C0237_initUserPath():
    InsertSection("check the ALWAYS_SET_PATH set in /etc/login.defs")
    ALWAYS_SET = 'unset'
    with open('/etc/login.defs', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('ALWAYS_SET_PATH', line) and not re.match('^#|^$', line):
                ALWAYS_SET = 'wrong'
                if re.search('yes', line):
                    ALWAYS_SET = 'right'


    if ALWAYS_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0237\n")
        logger.warning(f"WRN_C0237_01: %s", WRN_C0237_01)
        logger.warning("SUG_C0237: %s", SUG_C0237)
        Display("- No ALWAYS_SET_PATH config set...", "WARNING")
    elif ALWAYS_SET == 'right':
        logger.info("Has ALWAYS_SET_PATH set, checking OK")
        Display("- Check the ALWAYS_SET_PATH...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0237\n")
        logger.warning("WRN_C0237_02: %s", WRN_C0237_02)
        logger.warning("SUG_C0237: %s", SUG_C0237)
        Display("- Wrong ALWAYS_SET_PATH config set...", "WARNING")
