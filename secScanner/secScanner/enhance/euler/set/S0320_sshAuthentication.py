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

def S0320_sshAuthentication():
    InsertSection("Set SSH authentication...")
    set_sshAuthentication = seconf.get('euler', 'set_sshAuthentication')
    if set_sshAuthentication == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            PasswordAuthentication_flag = 0
            PubkeyAuthentication_flag = 0
            AuthorizedKeysFile_flag = 0
            ChallengeResponse_flag = 0
            IgnoreRhosts_flag = 0
            HostbasedAuthentication = 0
            with open("/etc/ssh/sshd_config", 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("PasswordAuthentication", line):
                        if "yes" in line:
                            PasswordAuthentication_flag = 1
                        else:
                            PasswordAuthentication_flag = -1
                    if re.match("PubkeyAuthentication", line):
                        if "yes" in line:
                            PubkeyAuthentication_flag = 1
                        else:
                            PubkeyAuthentication_flag = -1
                    if re.match("AuthorizedKeysFile", line):
                        if ".ssh/authorized_keys" in line:
                            AuthorizedKeysFile_flag = 1
                        else:
                            AuthorizedKeysFile_flag = -1
                    if re.match("ChallengeResponseAuthentication", line):
                        if "yes" in line:
                            ChallengeResponse_flag = 1
                        else:
                            ChallengeResponse_flag = -1
                    if re.match("IgnoreRhosts", line):
                        if "yes" in line:
                            IgnoreRhosts_flag = 1
                        else:
                            IgnoreRhosts_flag = -1
                    if re.match("HostbasedAuthentication", line):
                        if "no" in line:
                            HostbasedAuthentication = 1
                        else:
                            HostbasedAuthentication = -1
            if PasswordAuthentication_flag == 1 and PubkeyAuthentication_flag == 1 and AuthorizedKeysFile_flag == 1 and ChallengeResponse_flag == 1 and IgnoreRhosts_flag == 1 and HostbasedAuthentication == 1:
                logger.info("Already set SSH authentication OK")
                Display("Already set SSH authentication OK...", "FINISHED")
                return 
            with open("/etc/ssh/sshd_config", 'w') as write_file:
                for line in lines:
                    if re.match("PasswordAuthentication", line) and PasswordAuthentication_flag == -1:
                        write_file.write("PasswordAuthentication yes\n")
                    elif re.match("PubkeyAuthentication", line) and PubkeyAuthentication_flag == -1:
                        write_file.write("PubkeyAuthentication yes\n")
                    elif re.match("AuthorizedKeysFile", line) and AuthorizedKeysFile_flag == -1:
                        write_file.write("AuthorizedKeysFile      .ssh/authorized_keys\n")
                    elif re.match("ChallengeResponseAuthentication", line) and ChallengeResponse_flag == -1:
                        write_file.write("ChallengeResponseAuthentication yes\n")
                    elif re.match("IgnoreRhosts", line) and IgnoreRhosts_flag == -1:
                        write_file.write("IgnoreRhosts yes\n")
                    elif re.match("HostbasedAuthentication", line) and HostbasedAuthentication == -1:
                        write_file.write("HostbasedAuthentication no\n")
                    else:
                        write_file.write(line)
            with open("/etc/ssh/sshd_config", 'a') as add_file:
                if PasswordAuthentication_flag == 0:
                    add_file.write("\nPasswordAuthentication yes\n")
                if PubkeyAuthentication_flag == 0:
                    add_file.write("\nPubkeyAuthentication yes\n")
                if AuthorizedKeysFile_flag == 0:
                    add_file.write("\nAuthorizedKeysFile      .ssh/authorized_keys\n")
                if ChallengeResponse_flag == 0:
                    add_file.write("\nChallengeResponseAuthentication yes\n")
                if IgnoreRhosts_flag == 0:
                    add_file.write("\nIgnoreRhosts yes\n")
                if HostbasedAuthentication == 0:
                    add_file.write("\nHostbasedAuthentication no\n")
            logger.info("Set SSH authentication ok")
            Display("Set SSH authentication successfully...", "FINISHED")
        else:
            logger.warning("file /etc/ssh/sshd_config does not exist")
            Display("- file /etc/ssh/sshd_config not exists...", "FAILED")


    else:
        Display("Skip set SSH authentication due to config file...", "SKIPPING")
