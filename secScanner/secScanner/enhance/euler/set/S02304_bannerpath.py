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
import shutil
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02304_bannerpath():
    '''
    Function: ensure that the banner path is configured correctly
    '''
    InsertSection("set the banner path...")
    set_flag = seconf.get('euler', 'set_bannerpath')
    if set_flag == 'yes':
        config_file = '/etc/ssh/sshd_config'
        banner_line = 'Banner /etc/issue.net\n'
        if not os.path.exists(config_file):
            logger.warning("file /etc/ssh/sshd_config does not exist")
            Display("- File /etc/ssh/sshd_config does not exist...", "FAILED")
        else:
            already_set = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*Banner\s+', line, re.IGNORECASE):
                        fields = line.strip().split()
                        if len(fields) > 1 and fields[1] == '/etc/issue.net' and os.path.exists('/etc/issue.net'):
                            already_set = True
            if already_set:
                logger.info("banner path is already set correctly")
                Display("- Already set the banner path correctly...", "SKIPPING")
            else:
                if not os.path.exists(config_file + '_bak'):
                    shutil.copy2(config_file, config_file + '_bak')
                add_bak_file(config_file + '_bak')
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                is_exist = 0
                for line in lines:
                    if re.match(r'\s*Banner\s+', line, re.IGNORECASE):
                        is_exist = 1
                if is_exist == 0:
                    with open(config_file, 'a') as add_file:
                        add_file.write('\n' + banner_line)
                else:
                    with open(config_file, 'w') as write_file:
                        for line in lines:
                            if re.match(r'\s*Banner\s+', line, re.IGNORECASE):
                                write_file.write(banner_line)
                            else:
                                write_file.write(line)
                if not os.path.exists('/etc/issue.net'):
                    with open('/etc/issue.net', 'a') as add_file:
                        add_file.write('Authorized users only. All activities may be monitored and reported.\n')
                    os.chmod('/etc/issue.net', 0o644)
                ret, res = subprocess.getstatusoutput('systemctl restart sshd')
                if ret != 0:
                    logger.warning(f"restart sshd service failed: {res}")
                check_ok = False
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\s*Banner\s+', line, re.IGNORECASE):
                            fields = line.strip().split()
                            if len(fields) > 1 and fields[1] == '/etc/issue.net' and os.path.exists('/etc/issue.net'):
                                check_ok = True
                if check_ok:
                    logger.info("set the banner path successfully")
                    Display("- Set the banner path...", "FINISHED")
                else:
                    logger.warning("set the banner path failed")
                    Display("- Set the banner path...", "FAILED")
    else:
        Display("- Skip set the banner path...", "SKIPPING")

