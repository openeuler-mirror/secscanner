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
import os
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C35_nologinList():
    InsertSection("check list of users prohibited from login")
    check_flag_sys = False
    check_flag_paswd = False
    with open("/etc/pam.d/system-auth", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('pam_listfile.so', line):
                check_flag_sys = True

    with open('/etc/pam.d/password-auth', 'r') as read_file:
        lines = read_file.readlines()
        for line in lines:
            if re.match('auth', line) and re.search('pam_listfile.so', line):
                check_flag_paswd = True

    if not check_flag_sys and not check_flag_paswd:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC35\n")
        logger.warning("WRN_C35_01: %s", WRN_C35_01)
        logger.warning("SUG_C35: %s", SUG_C35)
        Display("- No list of users prohibited from login set...", "WARNING")
    elif not os.path.exists('/etc/login.user.deny'):
        with open(RESULT_FILE, "a") as file:
            file.write("\nC35\n")
        logger.warning("WRN_C35_02: %s", WRN_C35_02)
        logger.warning("SUG_C35: %s", SUG_C35)
        Display("- No path /etc/login.user.deny...", "WARNING")
    else:
        logger.info("Has list of users prohibited from login set, checking OK")
        Display("- Check the list of users prohibited from login...", "OK")
