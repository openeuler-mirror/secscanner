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
logger = logging.getLogger("secscanner")

# 从/etc/passwd文件中获取用户组
def get_user_groups_from_passwd(passwd_path):
    with open(passwd_path, 'r') as passwd_file:
        for line in passwd_file:
            fields = line.split(':')
            if len(fields) < 7:
                continue
            username = fields[0]
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

def S0207_passwdGroupexists():
    InsertSection("Ensure that all groups in/etc/passwd exist")
    passwd_group_exists = seconf.get('euler', 'passwd_group_exists')
    passwd_path = "/etc/passwd"
    group_path = "/etc/group"
    passwd_bak = "/etc/passwd_bak"
    group_bak  = "/etc/group_bak"
    counter = 0
    check = 0
    
    if passwd_group_exists == 'yes':
        if os.path.exists(passwd_path) and os.path.exists(group_path):
            if not os.path.exists(passwd_bak):
                shutil.copy2(passwd_path, passwd_bak)
            add_bak_file(passwd_bak)
            if not os.path.exists(group_bak):
                shutil.copy2(group_path, group_bak)
            add_bak_file(group_bak)
            for user, user_group in get_user_groups_from_passwd(passwd_path):
                if not check_group_in_group(group_path, user_group):
                    ret, result = subprocess.getstatusoutput(f'userdel -r {user}')
                    if ret != 0:
                        counter = -1
                        pass
                    else:
                        counter += 1
            if counter >= 0:
                for user, user_group in get_user_groups_from_passwd(passwd_path):
                    if not check_group_in_group(group_path, user_group):
                        check += 1

                if check == 0:
                    logger.info("Ensure that all groups in/etc/passwd exist")
                    Display("- Ensure that all groups in/etc/passwd exist...", "FINISHED")

                else:
                    logger.warning("The group in /etc/passwd does not exist in /etc/group")
                    Display("- The group in /etc/passwd does not exist in /etc/group ...", "FAILED")
            else:
                logger.warning("The execution of the userdel command failed")
                Display("- The execution of the userdel command failed ...", "FAILED")
        else:
            logger.warning("file /etc/group or /etc/passwd does not exist")
            Display("- file /etc/group or /etc/passwd does not exist...", "SKIPPING")
    else:
        Display("- Skip ensure that all groups in/etc/passwd exist due to config file...", "SKIPPING")


