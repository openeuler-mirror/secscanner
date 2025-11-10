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
import logging
import shutil
from secScanner.commands.check_outprint import *
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

ssh_protocol = seconf.get('level3', 'ssh_protocol')

def S135_sshProtocol():
    InsertSection("Set the ssh Protocol...")
    if ssh_protocol == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')

            exist_protocol = False
            with open('/etc/ssh/sshd_config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('Protocol', line) and re.search('2', line):
                        exist_protocol = True

            if not exist_protocol:
                with open('/etc/ssh/sshd_config', 'a') as add_file:
                    add_file.write('\nProtocol 2\n')
            else:
                with open('/etc/ssh/sshd_config', 'w') as write_file:
                    for line in lines:
                        if re.match('Protocol', line):
                            write_file.write("Protocol 2\n")
                        else:
                            write_file.write(line)

            check_exist = False
            with open('/etc/ssh/sshd_config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('Protocol', line) and re.search('2', line):
                        temp = line.strip('\n').split()
                        if temp[0] == 'Protocol' and temp[1] == '2':
                            check_exist = True

            if not check_exist:
                logger.warning("set the ssh Protocol failed, no set option")
                Display("- Set the ssh Protocol...", "FAILED")
            else:
                logger.info("set the ssh Protocol successfully")
                Display("- Set the ssh Protocol...", "FINISHED")

        else:   
            logger.warning("file /etc/ssh/sshd_config does not exist")
            Display("- file /etc/ssh/sshd_config does not exist...", "SKIPPING")
    else:
        Display("- Skip set ssh Protocol due to config file...", "SKIPPING")
