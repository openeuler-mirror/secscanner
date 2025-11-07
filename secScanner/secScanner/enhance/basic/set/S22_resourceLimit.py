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


def S22_resourceLimit():
    SET_CORE_DUMP= seconf.get('basic', 'set_core_dump')
    InsertSection("Set the coredump...")
    if SET_CORE_DUMP == 'yes':
        if os.path.exists('/etc/security/limits.conf') and not os.path.exists('/etc/security/limits.conf_bak'):
            shutil.copy2('/etc/security/limits.conf', '/etc/security/limits.conf_bak')
        add_bak_file('/etc/security/limits.conf_bak')
        if os.path.exists('/etc/security/limits.conf'):
            IS_EXIST = 0
            IS_EXIST2 = 0
            with open('/etc/security/limits.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('soft', line) and re.search('core', line):
                        IS_EXIST = 1
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('core', line):
                        IS_EXIST2 = 1

            if IS_EXIST == 0:
                with open('/etc/security/limits.conf', 'a') as add_file:
                    add_file.write("\n*               soft    core            0\n")
            else:
                with open('/etc/security/limits.conf', 'w') as write_file:
                    for line in lines:
                        if re.search('soft', line) and re.search('core', line):
                            write_file.write("*               soft    core            0\n")
                        else:
                            write_file.write(line)

            if IS_EXIST2 == 0:
                with open('/etc/security/limits.conf', 'a') as add_file:
                    add_file.write("\n*               hard    core            0\n")
            else:
                with open('/etc/security/limits.conf', 'w') as write_file:
                    for line in lines:
                        if re.search('hard', line) and re.search('core', line):
                            write_file.write("*               hard    core            0\n")
                        else:
                            write_file.write(line)
            logger.info("set the soft/hard core limit successfully")
            Display("- Setting the soft/hard core limit...", "FINISHED")
        else:
            logger.info("no filepath /etc/security/limits.conf")
            Display("- no filepath /etc/security/limits.conf...", "SKIPPING")
    else:
        Display("- Skip set coredump due to config file...", "SKIPPING")
