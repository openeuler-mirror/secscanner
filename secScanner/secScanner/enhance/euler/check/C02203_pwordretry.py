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

def C02203_pwordretry():
    '''
    Function: check verifying the old password when users change their own password
    '''
    InsertSection("check verifying the old password when users change their own password")
    if os.path.exists('/etc/pam.d/system-auth'):
        system_auth_found = False
        with open('/etc/pam.d/system-auth', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line):
                    system_auth_found = True
        password_auth_found = True
        if os.path.exists('/etc/pam.d/password-auth'):
            password_auth_found = False
            with open('/etc/pam.d/password-auth', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_unix.so', line):
                        password_auth_found = True
        if system_auth_found and password_auth_found:
            logger.info("pam_unix is enabled in the PAM password stack, checking ok")
            Display("- Has pam_unix set in the PAM password stack, the old password will be verified...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02203\n")
            logger.warning("WRN_C02203: %s", WRN_C02203)
            logger.warning("SUG_C02203: %s", SUG_C02203)
            Display("- No pam_unix set in the PAM password stack...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02203\n")
        logger.warning("WRN_C02203: /etc/pam.d/system-auth %s", WRN_no_file)
        logger.warning("SUG_C02203: /etc/pam.d/system-auth %s", SUG_no_file)
        Display("- Config file /etc/pam.d/system-auth not found...", "SKIPPING")

