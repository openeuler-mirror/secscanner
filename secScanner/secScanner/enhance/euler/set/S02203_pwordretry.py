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


def S02203_pwordretry():
    '''
    Function: ensure pam_unix.so is enabled to verify the old password when users change their own password
    '''
    InsertSection("set verifying the old password when users change their own password...")
    set_flag = seconf.get('euler', 'set_pwordretry')
    if set_flag == 'yes':
        pam_line = 'password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok\n'
        config_files = ['/etc/pam.d/system-auth', '/etc/pam.d/password-auth']
        already_set = True
        for config_file in config_files:
            if os.path.exists(config_file):
                found = False
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match('password', line) and re.search('pam_unix.so', line):
                            found = True
                if not found:
                    already_set = False
        if already_set:
            logger.info("pam_unix.so is already enabled in the PAM password stack")
            Display("- Already set pam_unix.so in the PAM password stack...", "SKIPPING")
        else:
            for config_file in config_files:
                if os.path.exists(config_file):
                    if not os.path.exists(config_file + '_bak'):
                        shutil.copy2(config_file, config_file + '_bak')
                    add_bak_file(config_file + '_bak')
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                    found = False
                    for line in lines:
                        if re.match('password', line) and re.search('pam_unix.so', line):
                            found = True
                    if not found:
                        insert_index = None
                        for index, line in enumerate(lines):
                            if re.match('password', line) and re.search('pam_pwquality.so', line):
                                insert_index = index + 1
                        if insert_index is not None:
                            lines.insert(insert_index, pam_line)
                        else:
                            lines.append(pam_line)
                        with open(config_file, 'w') as write_file:
                            write_file.writelines(lines)
            check_ok = True
            for config_file in config_files:
                if os.path.exists(config_file):
                    found = False
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.match('password', line) and re.search('pam_unix.so', line):
                                found = True
                    if not found:
                        check_ok = False
            if check_ok:
                logger.info("set pam_unix.so in the PAM password stack successfully")
                Display("- Set pam_unix.so in the PAM password stack...", "FINISHED")
            else:
                logger.warning("set pam_unix.so in the PAM password stack failed")
                Display("- Set pam_unix.so in the PAM password stack...", "FAILED")
    else:
        Display("- Skip set verifying the old password when users change their own password...", "SKIPPING")

