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

'''
grep -qiP "^HISTSIZE" /etc/profile && sed -i "/^HISTSIZE/cHISTSIZE=100"
/etc/profile || echo -e "HISTSIZE=100" >> /etc/profile
source /etc/profile
echo "10.2.1 repaired"
'''
def S1021_histsize():
    InsertSection("Set histsize...")
    SET_HISTSIZE = seconf.get('level3', 'set_histsize')
    config_file = "/etc/profile"
    if SET_HISTSIZE == 'yes':
        if os.path.exists(config_file):
            if not os.path.exists('/etc/profile_bak'):
                shutil.copy2('/etc/profile', '/etc/profile_bak')
            add_bak_file('/etc/profile_bak')
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^HISTSIZE', line):
                        if line.strip() == 'HISTSIZE=100':
                            logger.info("HISTSIZE is already set")
                            Display("- HISTSIZE already set correctly...", "FINISHED")
                            return
            WRITE_FLAG = False
            with open(config_file, 'w') as write_file:
                for line in lines:
                    if re.search(r'^HISTSIZE', line):
                        write_file.write("HISTSIZE=100\n")
                        WRITE_FLAG = True
                    else:
                        write_file.write(line)
            if WRITE_FLAG == False:
                with open(config_file, 'a') as add_file:
                    add_file.write("\nHISTSIZE=100\n")
            FLAG = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^HISTSIZE=100', line):
                        logger.info("10.2.1 histsize is set")
                        FLAG = True
            if FLAG == False:
                logger.error("HISTSIZE set incorrectly")
                Display("- HISTSIZE set incorrectly...", "FAILED")
            else:
                logger.info("HISTSIZE set correctly")
                Display("- HISTSIZE set correctly...", "FINISHED")
        else:
            logger.error("Config file not found, HISTSIZE set incorrectly")
            Display("- Config file not found...", "FAILED")
    else:
        Display("- Skip set HISTSIZE due to config file...", "SKIPPING")



