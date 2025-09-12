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
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")

# 从/etc/passwd文件中获取用户组
def get_user_groups_from_passwd(passwd_path):
    with open(passwd_path, 'r') as passwd_file:
        for line in passwd_file:
            fields = line.split(':')
            if len(fields) < 7:
                continue
            username = fields[0]  # 保存用户名
            shell = fields[6]
            if shell == '/bin/false' or shell == '/sbin/nologin':
                continue
            group = fields[3]
            yield username, group

# 检查组是否在/etc/group文件中
def check_group_in_group(group_path, group):
    with open(group_path, 'r') as group_file:
        for line in group_file:
            if group in line:
                return True
    return False


def C0207_passwdGroupexists():
    InsertSection("check if all groups in /etc/passwd exist")
    passwd_path = "/etc/passwd"
    group_path = "/etc/group"
    counter = 0
    group_id = []
    username = []

    if os.path.exists(passwd_path) and os.path.exists(group_path):
        for user, user_group in get_user_groups_from_passwd(passwd_path):
            if not check_group_in_group(group_path, user_group):
                group_id.append(user_group)
                username.append(user)
                counter += 1

        if counter > 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0207\n")
            logger.warning(f"WRN_C0207_01: Group for user [{username}] not found")
            logger.warning("SUG_C0207_01: %s", SUG_C0207_01)
            Display("- Check if all groups in /etc/passwd exist...", "WARNING")
        else:
            logger.info("All groups in /etc/passwd exist, checking ok")
            Display("- Check if all groups in /etc/passwd exist...", "OK")
    else:
        logger.warning("WRN_C0207_02: %s", WRN_C0207_02)
        logger.warning("SUG_C0207_02: %s", SUG_C0207_02)
        Display("- file /etc/group or /etc/passwd does not exist...", "WARNING")
