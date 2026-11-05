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

def S03303_sshkex():
    """Set the SSH key exchange algorithms in sshd config file."""
    InsertSection("Set config of KexAlgorithms...")
    set_flag = seconf.get('euler', 'set_sshkex')
    if set_flag == 'yes':
        kex_value = seconf.get('euler', 'ssh_kexalgorithms_value')
        if not kex_value:
            kex_value = "curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256"
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            exist = False
            is_set = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("KexAlgorithms", line):
                        exist = True
                        temp = line.split()
                        if len(temp) >= 2 and temp[1] == kex_value:
                            is_set = True
            if exist and is_set:
                logger.info("Check set of KexAlgorithms right")
                Display("- Already right set KexAlgorithms in sshd config", "FINISHED")
                return
            if exist:
                with open("/etc/ssh/sshd_config", "w") as write_file:
                    for line in lines:
                        if re.match("KexAlgorithms", line):
                            write_file.write("KexAlgorithms " + kex_value + "\n")
                        else:
                            write_file.write(line)
            else:
                with open("/etc/ssh/sshd_config", "a") as add_file:
                    add_file.write("\nKexAlgorithms " + kex_value + "\n")
            flag = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("KexAlgorithms " + kex_value, line):
                        flag = True
                        break
            if flag:
                logger.info("Set KexAlgorithms finish")
                Display("- Set KexAlgorithms in sshd config and restart sshd service", "FINISHED")
            else:
                logger.warning("Set KexAlgorithms failed")
                Display("- Set KexAlgorithms in sshd config", "FAILED")
        else:
            logger.warning("sshd config file not exist")
            Display("- sshd config file not exist", "FAILED")
    else:
        Display("Skip set KexAlgorithms due to config file...", "SKIPPING")
