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


def S02406_sudoersscript():
    '''
    Function: ensure that the scripts in sudoers are not writable by low privilege users
    '''
    InsertSection("set the scripts in sudoers not to be writable by low privilege users...")
    set_flag = seconf.get('euler', 'set_sudoersscript')
    if set_flag == 'yes':
        if not os.path.exists('/etc/sudoers'):
            logger.warning("file /etc/sudoers does not exist")
            Display("- File /etc/sudoers does not exist...", "FAILED")
        else:
            bad_scripts = []
            with open('/etc/sudoers', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match(r'\s*#', line) and re.search(r'\(root\)|\(ALL', line):
                        fields = line.split()
                        cmd_index = -1
                        for index, field in enumerate(fields):
                            if '(' in field:
                                cmd_index = index
                                break
                        if cmd_index < 0:
                            continue
                        cmd_str = ' '.join(fields[cmd_index+1:]).replace('NOPASSWD:', '')
                        for item in cmd_str.split(','):
                            item = item.strip()
                            if not item:
                                continue
                            cmd_path = item.split()[0].strip('"')
                            if not cmd_path.startswith('/'):
                                continue
                            if os.path.exists(cmd_path):
                                stat_info = os.stat(cmd_path)
                                if (stat_info.st_mode & 0o022) or (stat_info.st_mode & 0o200 and stat_info.st_uid != 0):
                                    if cmd_path not in bad_scripts:
                                        bad_scripts.append(cmd_path)
            if not bad_scripts:
                logger.info("no script in sudoers is writable by low privilege users")
                Display("- Already set the scripts in sudoers not to be writable by low privilege users...", "SKIPPING")
            else:
                for bad_script in bad_scripts:
                    stat_info = os.stat(bad_script)
                    os.chmod(bad_script, stat_info.st_mode & ~0o222)
                    logger.info(f"remove the write permission of low privilege users from {bad_script}")
                check_ok = True
                for bad_script in bad_scripts:
                    stat_info = os.stat(bad_script)
                    if (stat_info.st_mode & 0o022) or (stat_info.st_mode & 0o200 and stat_info.st_uid != 0):
                        check_ok = False
                if check_ok:
                    logger.info("set the scripts in sudoers not to be writable by low privilege users successfully")
                    Display("- Set the scripts in sudoers not to be writable by low privilege users...", "FINISHED")
                else:
                    logger.warning("set the scripts in sudoers not to be writable by low privilege users failed")
                    Display("- Set the scripts in sudoers not to be writable by low privilege users...", "FAILED")
    else:
        Display("- Skip set the scripts in sudoers not to be writable by low privilege users...", "SKIPPING")

