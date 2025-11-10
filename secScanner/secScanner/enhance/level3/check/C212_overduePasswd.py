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
from secScanner.gconfig import *
from secScanner.lib import *
import time
logger = logging.getLogger("secscanner")

def C212_overduePasswd():
    InsertSection("check for expired password")
    if os.path.exists('/etc/shadow'):
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
                print(username)

        if expired_found:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC212\n")
            logger.warning("WRN_C212_01: %s", WRN_C212_01)
            logger.warning("SUG_C212_01: %s", SUG_C212_01)
            Display("- At least one password has expired", "WARNING")
        else:
            logger.info('No expired password exists, checking ok')
            Display("- No expired password exists", "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC212\n")
        logger.warning("WRN_C212_02: %s", WRN_C212_02)
        logger.warning("SUG_C212_02: %s", SUG_C212_02)
        Display(f"- file /etc/shadow dose not exist...", "WARNING")

