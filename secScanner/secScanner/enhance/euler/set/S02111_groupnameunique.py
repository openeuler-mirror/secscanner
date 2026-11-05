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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S02111_groupnameunique():
    '''
    Function: Remove the duplicate group names in /etc/group
    '''
    set_flag = seconf.get('euler', 'set_groupnameunique')
    InsertSection("Ensure that the group name is unique")
    if set_flag == 'yes':
        if os.path.exists('/etc/group'):
            with open('/etc/group', 'r') as group_file:
                lines = group_file.readlines()
            seen_groups = set()
            new_lines = []
            for line in lines:
                groupname = line.strip().split(':')[0]
                if groupname in seen_groups:
                    logger.info(f"Remove the duplicate group name {groupname} from /etc/group")
                    continue
                seen_groups.add(groupname)
                new_lines.append(line)
            if len(new_lines) != len(lines):
                if not os.path.exists('/etc/group_bak'):
                    shutil.copy2('/etc/group', '/etc/group_bak')
                add_bak_file('/etc/group_bak')
                with open('/etc/group', 'w') as group_file:
                    group_file.writelines(new_lines)
                logger.info("All duplicate group names have been removed from /etc/group.")
                Display("- All duplicate group names have been removed from /etc/group.", "FINISHED")
            else:
                logger.info("No duplicate group names found in /etc/group, no need to fix")
                Display("- No duplicate group names found in /etc/group...", "SKIPPING")
        else:
            logger.warning("file /etc/group does not exist")
            Display("- file /etc/group not exists...", "SKIPPING")
    else:
        Display("- Skip ensure that the group name is unique due to config file...", "SKIPPING")
