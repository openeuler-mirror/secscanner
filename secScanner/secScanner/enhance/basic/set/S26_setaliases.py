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
import shutil
logger = logging.getLogger("secscanner")


def S26_setaliases():
    InsertSection("Set ls and rm aliases...")
    set_bashrc_alias = seconf.get('basic', 'set_bashrc_alias')
    if set_bashrc_alias == 'yes':
        if os.path.exists('/root/.bashrc'):
            if not os.path.exists('/root/.bashrc_bak'):
                shutil.copy2('/root/.bashrc', '/root/.bashrc_bak')
            add_bak_file('/root/.bashrc_bak')

            config_ls = False
            config_rm = False
            config_userdel = False
            
            with open('/root/.bashrc', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search('alias ls', line) and not re.match('#|$', line):
                        config_ls = True
                    if re.search('alias rm', line) and not re.match('#|$', line):
                        config_rm = True
                    if re.search('alias userdel', line) and not re.match('#|$', line):
                        config_userdel = True

            if not config_rm:
                with open('/root/.bashrc', 'a') as add_file:
                    add_file.write("alias rm='rm -i'\n")

            if not config_ls:
                with open('/root/.bashrc', 'a') as add_file:
                    add_file.write("alias ls='ls -al'\n")

            if not config_userdel:
                with open('/root/.bashrc', 'a') as add_file:
                    add_file.write("alias userdel='userdel -r'\n")

            check_ls = 'unset'
            check_rm = 'unset'
            check_userdel = 'unset'

            with open('/root/.bashrc', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('alias rm', line):
                        check_rm = 'set'
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'alias rm' and temp[1] == '\'rm -i\'':
                            check_rm = 'right'

            with open('/root/.bashrc', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('alias ls', line):
                        check_ls = 'set'
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'alias ls' and temp[1] == '\'ls -al\'':
                            check_ls = 'right'
            
            with open('/root/.bashrc', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('alias userdel', line):
                        check_userdel = 'set'
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'alias userdel' and temp[1] == '\'userdel -r\'':
                            check_userdel = 'right'

            if check_ls == 'unset' and check_rm == 'unset' and check_userdel == 'unset':
                logger.info("set ls and rm aliases failed, no set option")
                Display("- Set ls and rm aliases...", "FAILED")
            elif check_ls == 'right' and check_rm == 'right' and check_userdel == 'right':
                logger.info("set ls and rm aliases successfully")
                Display("- Set ls and rm aliases...", "FINISHED")
            else:
                logger.info("set ls and rm aliases failed, wrong setting")
                Display("- Set ls and rm aliases...", "FAILED")
        else:
            Display("- file '/root/.bashrc' does not exist...", "SKIPPING")
    else:
        Display("- Skip set ls and rm aliases due to config file...", "SKIPPING")
