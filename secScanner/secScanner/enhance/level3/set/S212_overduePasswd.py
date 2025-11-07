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
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
import time
logger = logging.getLogger("secscanner")

def S212_overduePasswd():
    InsertSection("Delete expired password")
    overdue_passwd = seconf.get('level3', 'overdue_passwd')
    if overdue_passwd == 'yes':
        if os.path.exists('/etc/shadow'):
            if not os.path.exists('/etc/shadow_bak'):
                shutil.copy2('/etc/shadow', '/etc/shadow_bak')
            add_bak_file('/etc/shadow_bak')

            expired_found = False
            with open('/etc/shadow', 'r') as read_file:
                lines = read_file.readlines()

            for line in lines:
                parts = line.split(':')
                if len(parts) < 8:
                    continue  # 跳过格式不正确的行

                username = parts[0]
                password = parts[1]
                last_change = parts[2]
                password_max_age = parts[4]

                if not last_change:
                    continue
                if not password_max_age:
                    continue
                
                last_change_int = int(last_change)
                password_max_age_int = int(password_max_age)

                # 计算当前日期和自上次密码更改以来的秒数
                current_date = int(time.time())
                seconds_last_change = last_change_int * 86400  # 转换为秒
                seconds_since_last_change = current_date - seconds_last_change
                password_max_age_seconds = password_max_age_int * 86400  # 转换为秒

                # 检查密码是否已过期
                if seconds_since_last_change > password_max_age_seconds and password != '!' and password != '*':
                    expired_found = True
                    ret, result = subprocess.getstatusoutput(f'userdel -r {username}')
                    if ret == 0:
                        expired_found = False
                
            if expired_found:
                logger.warning('At least one password has expired.')
                Display("- At least one password has expired", "FAILED")
            else:
                logger.info('No expired password exists')
                Display("- No expired password exists", "FINISHED")
    
        else:
            logger.warning(f"file /etc/shadow dose not exist")
            Display(f"- file /etc/shadow dose not exist...", "SKIPPING")
    
    else:
        Display("- Skip check for expired passwordsdue to config file...", "SKIPPING")

