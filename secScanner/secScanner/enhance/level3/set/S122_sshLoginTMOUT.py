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
import socket
logger = logging.getLogger("secscanner")

def S122_sshLoginTMOUT():
    InsertSection("Set the SSH login timeout...")
    ssh_login_tmout = seconf.get('level3', 'ssh_login_tmout')
    val_clientaliveinterval = seconf.get('level3', 'val_clientaliveinterval')
    if ssh_login_tmout == 'yes':
        if os.path.exists('/etc/ssh/sshd_config'):
            if not os.path.exists('/etc/ssh/sshd_config_bak'):
                shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
            add_bak_file('/etc/ssh/sshd_config_bak')
            
            with open('/etc/ssh/sshd_config', 'r+') as f:
                lines = f.readlines()
                ClientAliveInterval_exists = False
                ClientAliveCountMax_exists = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#ClientAliveInterval"):
                        ClientAliveInterval_exists = True
                        lines[i] = lines[i].replace("#", "")
                        if not re.search(val_clientaliveinterval, line):
                            lines[i] = f"ClientAliveInterval {val_clientaliveinterval}\n"
                        continue
                    elif line.strip().startswith("ClientAliveInterval"):
                        ClientAliveInterval_exists = True
                        if not re.search(val_clientaliveinterval, line):
                            lines[i] = f"ClientAliveInterval {val_clientaliveinterval}\n"
                        continue

                    if line.strip().startswith("#ClientAliveCountMax"):
                        ClientAliveCountMax_exists = True
                        lines[i] = lines[i].replace("#", "")
                        if not re.search('0', line):
                            lines[i] = "ClientAliveCountMax 0\n"
                        break
                    elif line.strip().startswith("ClientAliveCountMax"):
                        ClientAliveCountMax_exists = True
                        if not re.search('0', line):
                            lines[i] = "ClientAliveCountMax 0\n"
                        break

                if not ClientAliveInterval_exists:
                    lines.append(f"ClientAliveInterval {val_clientaliveinterval}\n")
                if not ClientAliveCountMax_exists:
                    lines.append("ClientAliveCountMax 0\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            check_interval = False
            check_countmax = False

            with open('/etc/ssh/sshd_config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('ClientAliveInterval', line):
                        tmp = line.split()
                        if tmp[0] == 'ClientAliveInterval' and tmp[1] == val_clientaliveinterval:
                            check_interval = True
                    if re.match('ClientAliveCountMax', line):
                        tmp = line.split()
                        if tmp[0] == 'ClientAliveCountMax' and tmp[1] == '0':
                            check_countmax = True

            if ClientAliveInterval_exists and ClientAliveCountMax_exists:
                if check_interval and check_countmax:
                    logger.info("set the ssh login timeout successfully")
                    Display("- Set the ssh loglevel...", "FINISHED")
                elif not check_interval:
                    logger.warning("set the ssh config ClientAliveInterval failed, no set option")
                    Display("- Set the ssh login timeout...", "FAILED")
                elif not check_countmax:
                    logger.warning("set the ssh config ClientAliveCountMax failed, no set option")
                    Display("- Set the ssh login timeout...", "FAILED")
                else:
                    logger.warning("set the ssh login timeout failed")
                    Display("- Set the ssh login timeout...", "FAILED")
            elif not ClientAliveInterval_exists:
                logger.warning("set the ssh login timeout failed, no ClientAliveInterval option")
                Display("- Set the ssh login timeout...", "FAILED")
            elif not ClientAliveCountMax_exists:
                logger.warning("set the ssh login timeout failed, no ClientAliveCountMax option")
                Display("- Set the ssh login timeout...", "FAILED")
            else:
                logger.warning("set the ssh login timeout failed")
                Display("- Set the ssh login timeout...", "FAILED")
        else:
            logger.warning(f"file /etc/ssh/sshd_config not exists")
            Display(f"- file /etc/ssh/sshd_config not exists...", "SKIPPING")
    else:
        Display("- Skip set ssh config login timeout due to config file...", "SKIPPING")

            

