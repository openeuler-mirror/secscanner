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


def C0233_noOneSU():
    InsertSection("check if permit user can su to root")
    # LINE_NUMBER = 0 # dont need to record line number
    IS_EXIST = 0
    with open('/etc/pam.d/su', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.search('auth', line) and re.search('pam_wheel.so', line) and re.search('group=wheel', line):
                IS_EXIST = 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0233\n")
        logger.warning("WRN_C0233: %s", WRN_C0233)
        logger.warning("SUG_C0233: %s", SUG_C0233)
        Display("- There is no pam_wheel set, check warning","WARNING")
    else:
        logger.info("There have pam_wheel set, check OK")
        Display("- Check the pam.d/su setting...", "OK")

