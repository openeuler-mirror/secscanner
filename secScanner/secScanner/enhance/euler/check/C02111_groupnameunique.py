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
from secScanner.gconfig import *
from secScanner.lib import *
from collections import defaultdict
logger = logging.getLogger("secscanner")

# 定义一个函数来读取 /etc/group 文件并返回一个列表，其中每个元素是一行内容
def read_group_file():
    with open('/etc/group', 'r') as file:
        return file.readlines()

# 定义一个函数来处理 /etc/group 文件内容并找出出现次数大于1的组名及其出现次数
def find_duplicate_groups(lines):
    group_counts = defaultdict(int)

    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 1:
            groupname = parts[0]
            group_counts[groupname] += 1

    duplicate_groups = [(groupname, count) for groupname, count in group_counts.items() if count > 1]
    return duplicate_groups

def C02111_groupnameunique():
    '''
    Function: Check if the group name is unique
    '''
    InsertSection("Check if the group name is unique")
    if os.path.exists('/etc/group'):
        group_lines = read_group_file()
        duplicate_groups = find_duplicate_groups(group_lines)

        if duplicate_groups:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02111\n")
            logger.warning("WRN_C02111: %s", WRN_C02111)
            logger.warning("SUG_C02111: %s", SUG_C02111)
            Display("- Duplicate group names found in /etc/group ...", "WARNING")
        else:
            logger.info("No duplicate group names found in /etc/group, checking ok")
            Display("- No duplicate group names found in /etc/group...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02111\n")
        logger.warning(f"WRN_C02111: /etc/group {WRN_no_file}")
        logger.warning(f"SUG_C02111: /etc/group {SUG_no_file}")
        Display("- file /etc/group does not exist...", "SKIPPING")
