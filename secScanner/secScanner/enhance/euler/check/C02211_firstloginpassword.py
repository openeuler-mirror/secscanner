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

def C02211_firstloginpassword():
    '''
    Function: check that accounts are forced to change the password at first login
    '''
    InsertSection("check that accounts are forced to change the password at first login")
    if os.path.exists('/etc/passwd') and os.path.exists('/etc/shadow'):
        normal_users = []
        with open('/etc/passwd', 'r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(':')
                if len(fields) >= 3 and fields[2].isdigit() and int(fields[2]) >= 1000:
                    normal_users.append(fields[0])
        bad_users = []
        with open('/etc/shadow', 'r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(':')
                if len(fields) >= 3 and fields[0] in normal_users:
                    password_field = fields[1]
                    lastchg = fields[2]
                    if password_field.startswith('!') or password_field == '*' or password_field == '':
                        continue
                    if lastchg != '0':
                        bad_users.append(fields[0])
        if bad_users:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02211\n")
            logger.warning("WRN_C02211_01: %s", WRN_C02211_01)
            logger.warning("SUG_C02211_01: %s", SUG_C02211_01)
            Display(f"- Password of users {','.join(bad_users)} is not set to expired...", "WARNING")
        else:
            logger.info("all normal users are forced to change the password at first login, checking ok")
            Display("- All normal users are forced to change the password at first login...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02211\n")
        logger.warning("WRN_C02211: /etc/passwd or /etc/shadow %s", WRN_no_file)
        logger.warning("SUG_C02211: /etc/passwd or /etc/shadow %s", SUG_no_file)
        Display("- Config file: /etc/passwd or /etc/shadow not found...", "SKIPPING")

