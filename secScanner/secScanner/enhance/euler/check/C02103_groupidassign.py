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
from collections import defaultdict
logger = logging.getLogger("secscanner")

# 定义一个函数来读取 /etc/passwd 文件并返回一个列表，其中每个元素是一行内容
def read_passwd_file():
    with open('/etc/passwd', 'r') as file:
        return file.readlines()

# 定义一个函数来处理 /etc/passwd 文件内容并找出出现次数大于1的初始组ID及其出现次数（过滤root组，组ID为0属于例外场景）
def find_duplicate_gids(lines):
    gid_counts = defaultdict(int)

    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 4:
            gid = parts[3]
            gid_counts[gid] += 1

    duplicate_gids = [(gid, count) for gid, count in gid_counts.items() if count > 1 and gid != '0']
    return duplicate_gids

def C02103_groupidassign():
    '''
    Function: Check whether different accounts are assigned different initial group IDs
    '''
    InsertSection("Check whether different accounts are assigned different group IDs")
    if os.path.exists('/etc/passwd'):
        passwd_lines = read_passwd_file()
        duplicate_gids = find_duplicate_gids(passwd_lines)

        if duplicate_gids:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02103\n")
            logger.warning("WRN_C02103_01: %s", WRN_C02103_01)
            logger.warning("SUG_C02103_01: %s", SUG_C02103_01)
            Display("- Duplicate group IDs found in /etc/passwd ...", "WARNING")
        else:
            logger.info("No duplicate group IDs found in /etc/passwd, checking ok")
            Display("- No duplicate group IDs found in /etc/passwd...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02103\n")
        logger.warning(f"WRN_C02103: /etc/passwd {WRN_no_file}")
        logger.warning(f"SUG_C02103: /etc/passwd {SUG_no_file}")
        Display("- file /etc/passwd does not exist...", "SKIPPING")

    if os.path.exists('/etc/login.defs'):
        usergroups_enab_flag = False
        with open('/etc/login.defs', 'r') as read_file:
            for line in read_file:
                if re.match(r'^\s*USERGROUPS_ENAB\s+yes\b', line):
                    usergroups_enab_flag = True
        if usergroups_enab_flag:
            logger.info("USERGROUPS_ENAB is set to yes in /etc/login.defs, checking ok")
            Display("- Check the USERGROUPS_ENAB is set to yes in /etc/login.defs...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02103\n")
            logger.warning("WRN_C02103_02: %s", WRN_C02103_02)
            logger.warning("SUG_C02103_02: %s", SUG_C02103_02)
            Display("- Check the USERGROUPS_ENAB is not set to yes in /etc/login.defs...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02103\n")
        logger.warning(f"WRN_C02103: /etc/login.defs {WRN_no_file}")
        logger.warning(f"SUG_C02103: /etc/login.defs {SUG_no_file}")
        Display("- file /etc/login.defs does not exist...", "SKIPPING")
