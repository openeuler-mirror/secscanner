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


def S02204_pwordaccount():
    '''
    Function: ensure that the password does not contain the account string
    '''
    InsertSection("set that the password does not contain the account string...")
    set_flag = seconf.get('euler', 'set_pwordaccount')
    if set_flag == 'yes':
        pwquality_line = ('password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root '
                          'try_first_pass local_users_only retry=3 dcredit=0 ucredit=0 lcredit=0 ocredit=0\n')
        config_files = ['/etc/pam.d/system-auth', '/etc/pam.d/password-auth']
        already_set = True
        for config_file in config_files:
            if os.path.exists(config_file):
                enabled = False
                usercheck_zero = False
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match('password', line) and re.search('pam_pwquality.so', line):
                            enabled = True
                            if re.search('usercheck=0', line):
                                usercheck_zero = True
                if not enabled or usercheck_zero:
                    already_set = False
        if already_set:
            logger.info("pam_pwquality is enabled without usercheck=0 in all PAM password stacks")
            Display("- Already set that the password does not contain the account string...", "SKIPPING")
        else:
            for config_file in config_files:
                if os.path.exists(config_file):
                    if not os.path.exists(config_file + '_bak'):
                        shutil.copy2(config_file, config_file + '_bak')
                    add_bak_file(config_file + '_bak')
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                    enabled = False
                    new_lines = []
                    for line in lines:
                        if re.match('password', line) and re.search('pam_pwquality.so', line):
                            enabled = True
                            new_line = ' '.join([field for field in line.split() if field != 'usercheck=0'])
                            if not new_line.startswith('password'):
                                new_line = 'password ' + new_line
                            new_lines.append(new_line + '\n')
                        else:
                            new_lines.append(line)
                    if not enabled:
                        new_lines.append(pwquality_line)
                    with open(config_file, 'w') as write_file:
                        write_file.writelines(new_lines)
            check_ok = True
            for config_file in config_files:
                if os.path.exists(config_file):
                    enabled = False
                    usercheck_zero = False
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.match('password', line) and re.search('pam_pwquality.so', line):
                                enabled = True
                                if re.search('usercheck=0', line):
                                    usercheck_zero = True
                    if not enabled or usercheck_zero:
                        check_ok = False
            if check_ok:
                logger.info("set that the password does not contain the account string successfully")
                Display("- Set that the password does not contain the account string...", "FINISHED")
            else:
                logger.warning("set that the password does not contain the account string failed")
                Display("- Set that the password does not contain the account string...", "FAILED")
    else:
        Display("- Skip set that the password does not contain the account string...", "SKIPPING")

