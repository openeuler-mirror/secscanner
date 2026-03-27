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


def C33_noEmptyPasswd():
    InsertSection("check the ssh permit empty passwd")
    CONFIG_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('PermitEmptyPasswords', line) and not re.match('^#|^$', line):
                CONFIG_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'no':
                    CONFIG_SET = 'right'

    if CONFIG_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC33\n")
        logger.warning("WRN_C33_01: %s", WRN_C33_01)
        logger.warning("SUG_C33: %s", SUG_C33)
        Display("- No ssh PermitEmptyPasswords config set...", "WARNING")
    elif CONFIG_SET == 'right':
        logger.info("Has ssh PermitEmptyPasswords set, checking OK")
        Display("- Check the ssh PermitEmptyPasswords...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC33\n")
        logger.warning("WRN_C33_02: %s", WRN_C33_02)
        logger.warning("SUG_C33: %s", SUG_C33)
        Display("- Wrong ssh PermitEmptyPasswords config set...", "WARNING")
