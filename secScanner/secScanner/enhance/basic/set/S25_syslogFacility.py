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

def S25_syslogFacility():
    SET_SSH_SYSLOGFACILITY = seconf.get('basic', 'set_ssh_syslogfacility')
    logger = logging.getLogger("secscanner")
    InsertSection("Set the syslogfacility...")
    if SET_SSH_SYSLOGFACILITY == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        add_bak_file('/etc/ssh/sshd_config_bak')
        # -----------------set the syslogfacility----------------
        IS_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('SyslogFacility', line) and re.search('AUTH', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\nSyslogFacility AUTH\n')
        else:
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.match('SyslogFacility', line):
                        write_file.write("SyslogFacility AUTH\n")
                    else:
                        write_file.write(line)
        ##sed -i 's/^SyslogFacility[[:space:]]AUTHPRIV/#&/g' /etc/ssh/sshd_config ???????
        IS_EXIST = 0
        CHECK_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('SyslogFacility', line) and re.search('AUTH', line):
                    IS_EXIST = 1
                    temp = line.strip('\n').split()
                    if temp[0] == 'SyslogFacility' and temp[1] == 'AUTH':
                        CHECK_EXIST = 1
        if IS_EXIST == 0:
            logger.info("set the ssh syslogfacility failed, no set option")
            Display("- Set the ssh syslogfacility...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("set the ssh syslogfacility failed, wrong setting")
            Display("- Set the ssh syslogfacility...", "FAILED")
        else:
            logger.info("set the ssh syslogfacility successfully")
            Display("- Set the ssh syslogfacility...", "FINISHED")
    else:
        Display("- Skip set ssh syslogfacility due to config file...", "SKIPPING")



