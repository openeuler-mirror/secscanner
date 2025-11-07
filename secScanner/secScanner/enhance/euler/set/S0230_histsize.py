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
import logging
logger = logging.getLogger("secscanner")

def S0230_histsize():
    InsertSection("Set histsize...")
    SET_HISTSIZE = seconf.get('euler', 'set_histsize')
    config_file = "/etc/profile"
    if SET_HISTSIZE == 'yes':
        if os.path.exists('/etc/profile'):
            if not os.path.exists('/etc/profile_bak'):
                shutil.copy2('/etc/profile', '/etc/profile_bak')
            add_bak_file('/etc/profile_bak')
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()

            new_lines = []
            for line in lines:
                if line.startswith('HISTSIZE='):
                    new_line = 'HISTSIZE=100\n'
                else:
                    new_line = line
                new_lines.append(new_line)
            
            with open(config_file, 'w') as file:
                file.writelines(new_lines)

            is_exist = False
            right = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
            for line in lines:
                if re.match('HISTSIZE', line):
                    is_exist = True
                    temp = line.strip('\n').split('=')
                    if temp[0] == 'HISTSIZE' and temp[1] == '100':
                        right = True

            if is_exist and not right:
                logger.warning("HISTSIZE set incorrectly")
                Display("- HISTSIZE set incorrectly...", "FAILED")
            elif is_exist and right:
                logger.info("HISTSIZE set correctly")
                Display("- HISTSIZE set correctly...", "FINISHED")
            else:
                logger.warning("HISTSIZE does not exist")
                Display("- HISTSIZE does not exist...", "FAILED")

        else:
            logger.warning("file /etc/profile does not exist")
            Display("- file /etc/profile does not exist...","SKIPPING")

    else:
        Display("- Skip set HISTSIZE due to config file...", "SKIPPING")

