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

def S03301_sshversion():
    """Set the SSH service protocol version to 2 in sshd config file."""
    InsertSection("Set config of ssh protocol version...")
    set_flag = seconf.get('euler', 'set_sshversion')
    if set_flag == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            exist = False
            is_set = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("Protocol", line):
                        exist = True
                        temp = line.split()
                        if len(temp) >= 2 and temp[1] == "2":
                            is_set = True
            if exist and is_set:
                logger.info("Check set of ssh protocol version right")
                Display("- Already right set ssh protocol version in sshd config", "FINISHED")
                return
            if exist:
                with open("/etc/ssh/sshd_config", "w") as write_file:
                    for line in lines:
                        if re.match("Protocol", line):
                            write_file.write("Protocol 2\n")
                        else:
                            write_file.write(line)
            else:
                with open("/etc/ssh/sshd_config", "a") as add_file:
                    add_file.write("\nProtocol 2\n")
            flag = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("Protocol 2", line):
                        flag = True
                        break
            if flag:
                logger.info("Set ssh protocol version finish")
                Display("- Set Protocol 2 in sshd config and restart sshd service", "FINISHED")
            else:
                logger.warning("Set ssh protocol version failed")
                Display("- Set ssh protocol version in sshd config", "FAILED")
        else:
            logger.warning("sshd config file not exist")
            Display("- sshd config file not exist", "FAILED")
    else:
        Display("Skip set ssh protocol version due to config file...", "SKIPPING")
