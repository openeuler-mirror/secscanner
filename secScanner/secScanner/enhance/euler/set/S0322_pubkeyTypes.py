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

def S0322_pubkeyTypes():
    InsertSection("Set config of PubkeyAcceptedKeyTypes...")
    set_pubkeyTypes = seconf.get('euler', 'set_pubkeyTypes')
    if set_pubkeyTypes == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            types = ["ssh-ed25519", "ssh-ed25519-cert-v01@openssh.com", "rsa-sha2-256", "rsa-sha2-512"]
            types_string = ",".join(types)
            types_string = "PubkeyAcceptedKeyTypes " + types_string
            pubkey_flag = False
            flag = True
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("PubkeyAcceptedKeyTypes", line):
                        pubkey_flag = True
                        for single_type in types:
                            if single_type not in line:
                                flag = False
            if pubkey_flag:
                if flag:
                    logger.info("Already set PubkeyAcceptedKeyTypes OK")
                    Display("- Already set PubkeyAcceptedKeyTypes OK", "FINISHED")
                    return
                with open("/etc/ssh/sshd_config", "w") as write_file:
                    for line in lines:
                        if re.match("PubkeyAcceptedKeyTypes", line):
                            write_file.write(types_string)
                        else:
                            write_file.write(line)
            else:
                with open("/etc/ssh/sshd_config", "a") as add_file:
                    add_file.write(f"\n{types_string}\n")
            with open("/etc/ssh/sshd_config", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("PubkeyAcceptedKeyTypes", line):
                        pubkey_flag = True
                        for single_type in types:
                            if single_type not in line:
                                flag = False
            if pubkey_flag:
                if flag:
                    logger.info("Set PubkeyAcceptedKeyTypes")
                    Display("- Set PubkeyAcceptedKeyTypes", "FINISHED")
                    return
            else:
                logger.warning("Set PubkeyAcceptedKeyTypes failed")
                Display("- Set PubkeyAcceptedKeyTypes failed", "FAILED")
        else:
            logger.warning("sshd config file not exist")
            Display("- sshd config file not exist", "FAILED")

    else:
        Display("Skip set PubkeyAcceptedKeyTypes due to config file...", "SKIPPING")

