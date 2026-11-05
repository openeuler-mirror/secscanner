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

def S04111_logsizelimit():
    set_logsizelimit = seconf.get('euler', 'set_logsizelimit')
    InsertSection("Set the audit log size limit in /etc/audit/auditd.conf...")
    if set_logsizelimit == 'yes':
        config_file = '/etc/audit/auditd.conf'
        if not os.path.exists(config_file):
            Display(f"- {config_file} does not exist...", "SKIPPING")
            return
        MAX_LOG_FILE_VALUE = '8'
        MAX_LOG_FILE_VAL = ''
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                line_strip = line.strip()
                if line_strip == '' or line_strip.startswith('#'):
                    continue
                if re.match(r'max_log_file\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        MAX_LOG_FILE_VAL = temp[1].strip()
        if MAX_LOG_FILE_VAL.isdigit() and int(MAX_LOG_FILE_VAL) > 0:
            logger.info("the audit log size limit is already set")
            Display("- Set the audit log size limit...", "SKIPPING")
            return
        if not os.path.exists(f'{config_file}_bak'):
            shutil.copy2(config_file, f'{config_file}_bak')
        add_bak_file(f'{config_file}_bak')

        IS_EXIST = 0
        with open(config_file, 'w') as write_file:
            for line in lines:
                if (not re.match('#|$', line)) and re.match(r'max_log_file\s*=', line.strip(), re.IGNORECASE):
                    write_file.write(f'max_log_file = {MAX_LOG_FILE_VALUE}\n')
                    IS_EXIST = 1
                else:
                    write_file.write(line)
        if IS_EXIST == 0:
            with open(config_file, 'a') as add_file:
                add_file.write(f'\nmax_log_file = {MAX_LOG_FILE_VALUE}\n')

        ret_restart, res_restart = subprocess.getstatusoutput('service auditd restart')
        if ret_restart != 0:
            logger.error(f'Failed to restart the auditd :{res_restart}')
            Display("- Set the audit log size limit...", "FAILED")
            return
        MAX_LOG_FILE_RESULT = ''
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                line_strip = line.strip()
                if line_strip == '' or line_strip.startswith('#'):
                    continue
                if re.match(r'max_log_file\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        MAX_LOG_FILE_RESULT = temp[1].strip()
        if not MAX_LOG_FILE_RESULT.isdigit() or int(MAX_LOG_FILE_RESULT) <= 0:
            logger.info("the audit log size limit is not set correctly")
            Display("- Set the audit log size limit...", "FAILED")
        else:
            logger.info("the audit log size limit is set, checking ok")
            Display("- Set the audit log size limit...", "FINISHED")
    else:
        Display("- Skip set the audit log size limit due to config file...", "SKIPPING")
