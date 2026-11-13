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

def S01115_openfiles():
    '''
    Function: Set the open file limits in /etc/security/limits.conf
    '''
    set_flag = seconf.get('euler', 'set_openfiles')
    InsertSection("Set the open file limits in /etc/security/limits.conf...")

    if set_flag == 'yes':
        config_file = '/etc/security/limits.conf'
        if os.path.exists(config_file):
            if not os.path.exists(config_file + '_bak'):
                shutil.copy2(config_file, config_file + '_bak')
            add_bak_file(config_file + '_bak')

            exist = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    fields = line.split()
                    if len(fields) >= 4 and fields[0] == '*' and fields[1] == 'soft' and fields[2] == 'nofile':
                        exist = True
            if exist:
                logger.info("The open file limits have already been set")
                Display("- The open file limits have already been set...", "SKIPPING")
            else:
                with open(config_file, 'a') as add_file:
                    add_file.write("\n* soft nofile 2000\n")
                    add_file.write("* hard nofile 10000\n")

                flag = False
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\*\s+soft\s+nofile\s+2000', line.strip()):
                            flag = True
                if flag:
                    logger.info("Set the open file limits finished, checking ok")
                    Display("- Set the open file limits in limits.conf...", "FINISHED")
                else:
                    logger.warning("Set the open file limits failed")
                    Display("- Set the open file limits in limits.conf...", "FAILED")
        else:
            logger.warning("The config file /etc/security/limits.conf does not exist")
            Display("- The config file /etc/security/limits.conf does not exist...", "FAILED")
    else:
        Display("- Skip set the open file limits due to config file...", "SKIPPING")
