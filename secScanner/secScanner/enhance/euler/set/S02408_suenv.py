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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02408_suenv():
    '''
    Function: ensure that su command does not inherit the user PATH environment variable
    '''
    InsertSection("set su command not to inherit the user PATH environment variable...")
    set_flag = seconf.get('euler', 'set_suenv')
    if set_flag == 'yes':
        config_file = '/etc/login.defs'
        if not os.path.exists(config_file):
            logger.warning("file /etc/login.defs does not exist")
            Display("- File /etc/login.defs does not exist...", "FAILED")
        else:
            already_set = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*ALWAYS_SET_PATH\b', line) and not re.match(r'\s*#', line) \
                            and re.search(r'yes', line, re.IGNORECASE):
                        already_set = True
            if already_set:
                logger.info("ALWAYS_SET_PATH is already set to yes in /etc/login.defs")
                Display("- Already set ALWAYS_SET_PATH=yes in /etc/login.defs...", "SKIPPING")
            else:
                if not os.path.exists(config_file + '_bak'):
                    shutil.copy2(config_file, config_file + '_bak')
                add_bak_file(config_file + '_bak')
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                is_exist = 0
                for line in lines:
                    if re.match(r'\s*ALWAYS_SET_PATH\b', line) and not re.match(r'\s*#', line):
                        is_exist = 1
                if is_exist == 0:
                    with open(config_file, 'a') as add_file:
                        add_file.write('\nALWAYS_SET_PATH\t\tyes\n')
                else:
                    with open(config_file, 'w') as write_file:
                        for line in lines:
                            if re.match(r'\s*ALWAYS_SET_PATH\b', line) and not re.match(r'\s*#', line):
                                write_file.write('ALWAYS_SET_PATH\t\tyes\n')
                            else:
                                write_file.write(line)
                check_ok = False
                with open(config_file, 'r') as read_file:
                    check_lines = read_file.readlines()
                    for line in check_lines:
                        if re.match(r'\s*ALWAYS_SET_PATH\b', line) and not re.match(r'\s*#', line) \
                                and re.search(r'yes', line, re.IGNORECASE):
                            check_ok = True
                if check_ok:
                    logger.info("set ALWAYS_SET_PATH=yes in /etc/login.defs successfully")
                    Display("- Set ALWAYS_SET_PATH=yes in /etc/login.defs...", "FINISHED")
                else:
                    logger.warning("set ALWAYS_SET_PATH=yes in /etc/login.defs failed")
                    Display("- Set ALWAYS_SET_PATH=yes in /etc/login.defs...", "FAILED")
    else:
        Display("- Skip set su command not to inherit the user PATH environment variable...", "SKIPPING")

