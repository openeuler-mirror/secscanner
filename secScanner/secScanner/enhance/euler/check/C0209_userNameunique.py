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
from collections import defaultdict

logger = logging.getLogger("secscanner")

# 定义一个函数来读取 /etc/passwd 文件并返回一个列表，其中每个元素是一行内容
def read_passwd_file():
    with open('/etc/passwd', 'r') as file:
        return file.readlines()

# 定义一个函数来处理 /etc/passwd 文件内容并找出出现次数大于1的用户名及其出现次数
def find_duplicate_users(lines):
    user_counts = defaultdict(int)
    
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 1:
            username = parts[0]
            user_counts[username] += 1
    
    # 找出出现次数大于1的用户名及其出现次数
    duplicate_users = [(username, count) for username, count in user_counts.items() if count > 1]
    return duplicate_users

def C0209_userNameunique():
    InsertSection("Check if the account is unique")
    if os.path.exists('/etc/passwd'):
        passwd_lines = read_passwd_file()
        duplicate_users = find_duplicate_users(passwd_lines)

        if duplicate_users:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0209\n")
            logger.warning("WRN_C0209_01: %s", WRN_C0209_01)
            logger.warning("SUG_C0209_01: %s", SUG_C0209_01)
            Display("- Duplicate users found in /etc/passwd ...", "WARNING")
        else:
            logger.info("No duplicate users found in /etc/passwd, checking ok")
            Display("- No duplicate users found in /etc/passwd...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0209\n")
        logger.warning("WRN_C0209_02: %s", WRN_C0209_02)
        logger.warning("SUG_C0209_02: %s", SUG_C0209_02)
        Display("- file /etc/passwd dose not exist...", "WARNING")