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


import subprocess
import logging
import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0334_permitUserenv():
    InsertSection("Set config of permitUserenv...")
    set_permitUserenv = seconf.get('euler', 'set_permitUserenv')
    if set_permitUserenv == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            exist = False
            set = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("PermitUserEnvironment", line):
                        exist = True
                        if re.search("no", line):
                            set = True
            if exist and set:
                logger.info("Check set of PermitUserEnvironment right")
                Display("- Already right set PermitUserEnvironment in sshd config", "FINISHED")
                return
            if exist:
                with open("/etc/ssh/sshd_config", "w") as write_file:
                    for line in lines:
                        if re.match("PermitUserEnvironment", line):
                            write_file.write("PermitUserEnvironment no\n")
                        else:
                            write_file.write(line)
            else:
                with open("/etc/ssh/sshd_config", "a") as add_file:
                    add_file.write("\nPermitUserEnvironment no\n")
            flag = False
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("PermitUserEnvironment no", line):
                        flag = True
                        break
            if flag:
                logger.info("Set PermitUserEnvironment finish")
                Display("- Set PermitUserEnvironment in sshd config and restart sshd service", "FINISHED")
            else:
                logger.warning("Set PermitUserEnvironment failed")
                Display("- Set PermitUserEnvironment in sshd config", "FAILED")
        else:
            logger.warning("sshd config file not exist")
            Display("- sshd config file not exist", "FAILED")
    else:
        Display("Skip set PermitUserEnvironment due to config file...", "SKIPPING")
