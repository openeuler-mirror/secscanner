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


import logging
import os
import re
import shutil
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S04203_cronlog():
    set_cronlog = seconf.get('euler', 'set_cronlog')
    InsertSection("Set the cron service log in /etc/rsyslog.conf...")
    if set_cronlog == 'yes':
        config_file = '/etc/rsyslog.conf'
        if not os.path.exists(config_file):
            Display(f"- {config_file} does not exist...", "SKIPPING")
            return
        IS_EXIST = 0
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('/var/log/cron', line):
                    IS_EXIST = 1
        if IS_EXIST == 1:
            logger.info("the cron service log is already configured")
            Display("- Set the cron service log...", "SKIPPING")
            return
        if not os.path.exists(f'{config_file}_bak'):
            shutil.copy2(config_file, f'{config_file}_bak')
        add_bak_file(f'{config_file}_bak')
        with open(config_file, 'a') as add_file:
            add_file.write('\ncron.*                                                  /var/log/cron\n')

        ret_restart, res_restart = subprocess.getstatusoutput('systemctl restart rsyslog.service')
        if ret_restart != 0:
            logger.error(f'Failed to restart the rsyslog :{res_restart}')
            Display("- Set the cron service log...", "FAILED")
            return
        IS_RESULT = 0
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('/var/log/cron', line):
                    IS_RESULT = 1
        if IS_RESULT == 0:
            logger.info("the cron service log is not set correctly")
            Display("- Set the cron service log...", "FAILED")
        else:
            logger.info("the cron service log is set, checking ok")
            Display("- Set the cron service log...", "FINISHED")
    else:
        Display("- Skip set the cron service log due to config file...", "SKIPPING")
