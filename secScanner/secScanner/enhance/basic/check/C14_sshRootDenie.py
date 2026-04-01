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
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")


def C14_sshRootDenie():

    InsertSection("check the ssh root denie")
    OS_DISTRO = get_value("OS_DISTRO")
    if OS_DISTRO == '7':
        IS_EXIST = 0
        with open('/etc/securetty', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if re.search('pts/', line) and not re.match('^#|^$', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            Display("- Check the telnet deny...", "OK")
        else:
            Display("- Wrong Telnet Denie set...", "WARNING")

### check the SSH Root Denie
    SSH_ROOT_DENIE_SET = 'unset'
    with open('/etc/ssh/sshd_config', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('PermitRootLogin', line) and (not re.match('^#|^$', line)):
                SSH_ROOT_DENIE_SET = 'wrong'
                temp = line.split()
                if len(temp) == 2 and temp[1] == 'no':
                    SSH_ROOT_DENIE_SET = 'right'


    if SSH_ROOT_DENIE_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC14\n")
        logger.warning("WRN_C14_01: %s", WRN_C14_01)
        logger.warning("SUG_C14: %s", SUG_C14)
        Display("- No ssh Root denie set...", "WARNING")
    elif SSH_ROOT_DENIE_SET == 'right':
        logger.info("Has ssh Root denie set, checking OK")
        Display("- Check the ssh Root denie...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC14\n")
        logger.warning(f"WRN_C14_02: %s", WRN_C14_02)
        logger.warning("SUG_C14: %s", SUG_C14)
        Display("- Wrong ssh Root denie set...", "WARNING")
