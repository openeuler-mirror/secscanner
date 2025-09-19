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


from collections import defaultdict
import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil

logger = logging.getLogger("secscanner")


def S0209_userNameunique():
    InsertSection("Ensure that the account name is unique")
    account_name_unique = seconf.get('euler', 'account_name_unique')
    if account_name_unique == 'yes':
        if os.path.exists('/etc/passwd'):
            if not os.path.exists('/etc/passwd_bak'):
                shutil.copy2('/etc/passwd', '/etc/passwd_bak')
            add_bak_file('/etc/passwd_bak')
            with open('/etc/passwd', 'r') as passwd_file:
                lines = passwd_file.readlines()

            # 使用defaultdict来计数每个用户名出现的次数
            user_counts = defaultdict(int)
            # 用于存储每个用户的家目录
            home_dirs = {}

            for line in lines:

                parts = line.strip().split(':')
                if len(parts) >= 7:
                    username = parts[0]
                    home_dir = parts[5]
                    user_counts[username] += 1
                    home_dirs[username] = home_dir

            # 找出出现次数大于1的用户名及其家目录
            users_to_remove = [(username, home_dir) for username, home_dir in home_dirs.items() if user_counts[username] > 1 and os.path.isdir(home_dir)]

            # 从/etc/passwd中删除这些用户
            new_lines = [line for line in lines if line.split(':')[0] not in [username for username, _ in users_to_remove]]

            # 写入新的passwd文件内容
            with open('/etc/passwd', 'w') as passwd_file:
                passwd_file.writelines(new_lines)
            
            for username, home_dir in users_to_remove:
                try:
                    if os.path.exists(home_dir) and os.path.isdir(home_dir):
                        bak_dir = home_dir + '_bak'
                        shutil.copytree(home_dir, bak_dir)
                        shutil.rmtree(home_dir)
                        logger.info("Successfully deleted duplicate account {username} and {home_dir}")
                    else:
                        logger.warning(f"Home directory for user {username} at {home_dir} does not exist")
                except Exception as e:
                    logger.error(f"Error removing home directory for user {username}: {e}")
            
            if all(not (user_exists or dir_exists) for username, home_dir, user_exists, dir_exists in
                    [(username, home_dir, username in [line.split(':')[0] for line in new_lines],
                        os.path.exists(home_dir) and os.path.isdir(home_dir))
                        for username, home_dir in users_to_remove]):
                logger.info("All users and their home directories have been removed from the system.")
                Display("- All users and their home directories have been removed from the system.", "FINISHED")
            else:
                logger.warning("Failed to remove all users and their home directories from the system.")
                Display("-Failed to remove all users and their home directories from the system.", "FAILED")
        
        else:
            logger.warning("file /etc/passwd does not exist")
            Display("- file /etc/passwd not exists...", "SKIPPING")
    else:
        Display("- Skip ensure that the account name is unique due to config file...", "SKIPPING")
