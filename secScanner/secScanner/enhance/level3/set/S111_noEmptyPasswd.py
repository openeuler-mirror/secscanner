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


def S111_noEmptyPasswd():
    InsertSection("Set prohibit users with empty passwords")
    no_empty_passwd = seconf.get('level3', 'no_empty_passwd')
    if no_empty_passwd == 'yes':
        if not os.path.exists('/etc/shadow_bak') and os.path.exists('/etc/shadow'):
            shutil.copy2('/etc/shadow', '/etc/shadow_bak')
        add_bak_file('/etc/shadow_bak')
        if os.path.exists('/etc/shadow'):
            command = "awk -F: '($2 == \"\") { exit 1 }' /etc/shadow"
            command_username = "awk -F: '($2 == \"\") { print $1 }' /etc/shadow"
            ret, result = subprocess.getstatusoutput(command)
            if ret == 1:
                exit_code, username = subprocess.getstatusoutput(command_username) 
                if exit_code == 0:
                    username = username.strip().split('\n')
                    for user in username:
                        out, output = subprocess.getstatusoutput(f'passwd -l {user}')
                        if out == 0:
                            logger.info("Set the prohibit users with empty passwords")
                            Display("- Set prohibit users with empty passwords...", "FINISHED")
                        else:
                            logger.warning("User lock failed")
                            Display("- User lock failed...", "FAILED")
                else:
                    logger.warning("Failed to obtain empty password user")
                    Display("- Failed to obtain empty password user", "FAILED")
            else:
                logger.info("No empty password user, checking ok")
                Display("- No empty password user...", "FINISHED")
        else:
            logger.warning("file /etc/shadow does not exist")
            Display("- file /etc/shadow  not exists...", "SKIPPING")

    else:
        Display("- Skip prohibit users with empty passwords due to config file...", "SKIPPING")
