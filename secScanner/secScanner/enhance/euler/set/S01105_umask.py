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

def S01105_umask():
    '''
    Function: Set the UMASK config in /etc/bashrc
    '''
    set_flag = seconf.get('euler', 'set_umask')
    umask_value = seconf.get('euler', 'umask_value')
    InsertSection("Set the UMASK in /etc/bashrc...")

    if set_flag == 'yes':
        config_file = '/etc/bashrc'
        if os.path.exists(config_file):
            if not os.path.exists(config_file + '_bak'):
                shutil.copy2(config_file, config_file + '_bak')
            add_bak_file(config_file + '_bak')

            exist = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*umask\s', line):
                        exist = True
            if exist:
                with open(config_file, 'w') as write_file:
                    for line in lines:
                        if re.match(r'\s*umask\s', line):
                            write_file.write("umask %s\n" % umask_value)
                        else:
                            write_file.write(line)
            else:
                with open(config_file, 'a') as add_file:
                    add_file.write("\numask %s\n" % umask_value)

            flag = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    match = re.match(r'\s*umask\s+(\S+)', line)
                    if match:
                        try:
                            if int(match.group(1), 8) == int(umask_value, 8):
                                flag = True
                        except ValueError:
                            if match.group(1) == umask_value:
                                flag = True
            if flag:
                logger.info("Set the UMASK finished, checking ok")
                Display("- Set the UMASK in /etc/bashrc...", "FINISHED")
            else:
                logger.warning("Set the UMASK failed")
                Display("- Set the UMASK in /etc/bashrc...", "FAILED")
        else:
            logger.warning("The config file /etc/bashrc does not exist")
            Display("- The config file /etc/bashrc does not exist...", "FAILED")
    else:
        Display("- Skip set the UMASK due to config file...", "SKIPPING")
