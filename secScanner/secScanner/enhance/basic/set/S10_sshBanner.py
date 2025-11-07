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
import pathlib
logger = logging.getLogger("secscanner")


def S10_sshBanner():
    InsertSection("Set the sshbanner...")
    SET_SSH_LOGIN_BANNER = seconf.get('basic', 'set_ssh_login_banner')
    SSH_LOGIN_BANNER_VALUE = seconf.get('basic', 'ssh_login_banner_value')

    if SET_SSH_LOGIN_BANNER == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        add_bak_file('/etc/ssh/sshd_config_bak')
        if os.path.exists("/etc/sshbanner"):
            if not os.path.exists('/etc/sshbanner_bak'):
                shutil.copy2('/etc/sshbanner', '/etc/sshbanner_bak')
            add_bak_file('/etc/sshbanner_bak')
            logger.info("exist /etc/sshbanner file, rewrite it...")
            with open('/etc/sshbanner', 'w') as write_file:
                write_file.write(SSH_LOGIN_BANNER_VALUE)
                write_file.write('\n')
        else:
            logger.info("no /etc/sshbanner file, creating...")
            pathlib.Path('/etc/sshbanner').touch()
            os.chown('/etc/sshbanner', os.getuid(), os.getuid())##chown bin:bin /etc/sshbanner
            os.chmod('/etc/sshbanner', 644)
            with open('/etc/sshbanner', 'w') as write_file:
                write_file.write(SSH_LOGIN_BANNER_VALUE)
                write_file.write('\n')

        IS_EXIST = 0
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.search('Banner', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/ssh/sshd_config', 'a') as add_file:
                add_file.write('\nBanner /etc/sshbanner\n')
        else:
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.search('Banner', line):
                        write_file.write("Banner /etc/sshbanner\n")
                    else:
                        write_file.write(line)
        TMP_V = 0
        if os.path.exists('/etc/sshbanner'):
            with open('/etc/ssh/sshd_config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search('banner', line):
                        TMP_V = 1
            if TMP_V > 0:
                logger.info("set the sshdbanner successfully")
                Display("- Set the sshbanner...", "FINISHED")
        else:
            logger.info("create the sshdbanner failed")
            Display("- Set the sshbanner failed...", "FAILED")
    else:
        Display("- Skip set ssh login banner due to config file...", "SKIPPING")

