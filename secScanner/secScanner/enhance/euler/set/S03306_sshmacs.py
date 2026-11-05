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

def S03306_sshmacs():
    """Set the SSH message authentication codes algorithms in sshd config file."""
    InsertSection("Set config of MACs...")
    set_flag = seconf.get('euler', 'set_sshmacs')
    if set_flag == 'yes':
        macs_value = seconf.get('euler', 'ssh_macs_value')
        if not macs_value:
            macs_value = "hmac-sha2-512,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-256-etm@openssh.com"
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            exist = False
            is_set = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("MACs", line, re.IGNORECASE):
                        exist = True
                        temp = line.split()
                        if len(temp) >= 2 and temp[1] == macs_value:
                            is_set = True
            if exist and is_set:
                logger.info("Check set of MACs right")
                Display("- Already right set MACs in sshd config", "FINISHED")
                return
            if exist:
                with open("/etc/ssh/sshd_config", "w") as write_file:
                    for line in lines:
                        if re.match("MACs", line, re.IGNORECASE):
                            write_file.write("MACs " + macs_value + "\n")
                        else:
                            write_file.write(line)
            else:
                with open("/etc/ssh/sshd_config", "a") as add_file:
                    add_file.write("\nMACs " + macs_value + "\n")
            flag = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("MACs " + macs_value, line):
                        flag = True
                        break
            if flag:
                logger.info("Set MACs finish")
                Display("- Set MACs in sshd config and restart sshd service", "FINISHED")
            else:
                logger.warning("Set MACs failed")
                Display("- Set MACs in sshd config", "FAILED")
        else:
            logger.warning("sshd config file not exist")
            Display("- sshd config file not exist", "FAILED")
    else:
        Display("Skip set MACs due to config file...", "SKIPPING")
