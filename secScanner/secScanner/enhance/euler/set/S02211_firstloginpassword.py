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


import os
import re
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02211_firstloginpassword():
    '''
    Function: ensure that accounts are forced to change the password at first login
    '''
    InsertSection("set accounts to be forced to change the password at first login...")
    set_flag = seconf.get('euler', 'set_firstloginpassword')
    if set_flag == 'yes':
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
            if not bad_users:
                logger.info("all normal users are already forced to change the password at first login")
                Display("- Already set accounts to change the password at first login...", "SKIPPING")
            else:
                check_ok = True
                for bad_user in bad_users:
                    ret, res = subprocess.getstatusoutput(f'passwd -e {bad_user}')
                    if ret != 0:
                        check_ok = False
                        logger.warning(f"expire the password of {bad_user} failed: {res}")
                    else:
                        logger.info(f"expire the password of {bad_user} successfully")
                if check_ok:
                    logger.info("set accounts to change the password at first login successfully")
                    Display("- Set accounts to change the password at first login...", "FINISHED")
                else:
                    logger.warning("set accounts to change the password at first login failed")
                    Display("- Set accounts to change the password at first login...", "FAILED")
        else:
            logger.warning("file /etc/passwd or /etc/shadow does not exist")
            Display("- File /etc/passwd or /etc/shadow does not exist...", "FAILED")
    else:
        Display("- Skip set accounts to change the password at first login...", "SKIPPING")

