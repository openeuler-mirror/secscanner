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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S02103_groupidassign():
    '''
    Function: Set USERGROUPS_ENAB to yes to ensure each new account is assigned a unique group ID
    '''
    set_flag = seconf.get('euler', 'set_groupidassign')
    InsertSection("Ensure different accounts are assigned different group IDs...")
    if set_flag == 'yes':
        login_defs = '/etc/login.defs'
        if os.path.exists(login_defs):
            with open(login_defs, 'r') as file:
                lines = file.readlines()
            enab_index = -1
            enab_yes = False
            for i, line in enumerate(lines):
                if re.match(r'^\s*USERGROUPS_ENAB\s+', line):
                    enab_index = i
                    if re.match(r'^\s*USERGROUPS_ENAB\s+yes\b', line):
                        enab_yes = True
            if enab_yes:
                logger.info("USERGROUPS_ENAB is already set to yes in /etc/login.defs")
                Display("- USERGROUPS_ENAB is already set to yes...", "SKIPPING")
            else:
                bak_file = login_defs + '_bak'
                if not os.path.exists(bak_file):
                    shutil.copy2(login_defs, bak_file)
                add_bak_file(bak_file)
                if enab_index >= 0:
                    lines[enab_index] = 'USERGROUPS_ENAB yes\n'
                else:
                    lines.append('USERGROUPS_ENAB yes\n')
                with open(login_defs, 'w') as file:
                    file.writelines(lines)
                logger.info("Set USERGROUPS_ENAB to yes in /etc/login.defs, checking ok")
                Display("- Set USERGROUPS_ENAB to yes in /etc/login.defs...", "FINISHED")
        else:
            logger.warning("file /etc/login.defs does not exist")
            Display("- file /etc/login.defs not exists...", "SKIPPING")
    else:
        Display("- Skip ensure different accounts are assigned different group IDs due to config file...", "SKIPPING")
