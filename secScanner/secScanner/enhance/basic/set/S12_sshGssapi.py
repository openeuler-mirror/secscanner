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
import logging
import shutil
logger = logging.getLogger("secscanner")


def S12_sshGssapi():
    InsertSection("Set the gssapi...")
    SET_SSH_GSSAPI = seconf.get('basic', 'set_ssh_gssapi')

    if SET_SSH_GSSAPI == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        add_bak_file('/etc/ssh/sshd_config_bak')
        IS_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#|$', line) and re.match('GSSAPIAuthentication', line):
                    IS_EXIST = 1

        if IS_EXIST == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write("\nGSSAPIAuthentication no\n")
        else:
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.search('GSSAPIAuthentication', line):
                        write_file.write("GSSAPIAuthentication no\n")
                    else:
                        write_file.write(line)

        GSSAPI_SET = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#|$', line) and re.search('GSSAPIAuthentication', line):
                    IS_EXIST = 1
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1] == 'no':
                        GSSAPI_SET = 1

        if IS_EXIST == 0:
            logger.info("set the ssh gssapi failed, no set options")
            Display("- Set the ssh gssapi...", "FAILED")
        elif IS_EXIST == 1 and GSSAPI_SET == 0:
            logger.info("set the ssh gssapi failed, wrong setting")
            Display("- Set the ssh gssapi...", "FAILED")
        elif IS_EXIST == 1 and GSSAPI_SET == 1:
            logger.info("set the ssh gssapi successfully")
            Display("- Set the ssh gssapi...", "FINISHED")
        else:
            pass
    else:
        Display(f"- Skip set ssh gssapi due to config file...", "SKIPPING")
