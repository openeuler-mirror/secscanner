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

def S04102_auditrotate():
    set_auditrotate = seconf.get('euler', 'set_auditrotate')
    InsertSection("Set the audit log rotate in /etc/audit/auditd.conf...")
    if set_auditrotate == 'yes':
        config_file = '/etc/audit/auditd.conf'
        if not os.path.exists(config_file):
            Display(f"- {config_file} does not exist...", "SKIPPING")
            return
        ACTION_VALUE = 'ROTATE'
        NUM_LOGS_VALUE = '5'
        ACTION_VAL = ''
        NUM_LOGS_VAL = ''
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                line_strip = line.strip()
                if line_strip == '' or line_strip.startswith('#'):
                    continue
                if re.match(r'max_log_file_action\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        ACTION_VAL = temp[1].strip()
                if re.match(r'num_logs\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        NUM_LOGS_VAL = temp[1].strip()
        if ACTION_VAL.upper() in ('ROTATE', 'KEEP_LOGS') and NUM_LOGS_VAL.isdigit() and 2 <= int(NUM_LOGS_VAL) <= 99:
            logger.info("the audit log rotate is already set")
            Display("- Set the audit log rotate...", "SKIPPING")
            return
        if not os.path.exists(f'{config_file}_bak'):
            shutil.copy2(config_file, f'{config_file}_bak')
        add_bak_file(f'{config_file}_bak')

        ACTION_EXIST = 0
        NUM_EXIST = 0
        with open(config_file, 'w') as write_file:
            for line in lines:
                if (not re.match('#|$', line)) and re.search('max_log_file_action', line, re.IGNORECASE):
                    write_file.write(f'max_log_file_action = {ACTION_VALUE}\n')
                    ACTION_EXIST = 1
                elif (not re.match('#|$', line)) and re.search('num_logs', line, re.IGNORECASE):
                    write_file.write(f'num_logs = {NUM_LOGS_VALUE}\n')
                    NUM_EXIST = 1
                else:
                    write_file.write(line)
        if ACTION_EXIST == 0:
            with open(config_file, 'a') as add_file:
                add_file.write(f'\nmax_log_file_action = {ACTION_VALUE}\n')
        if NUM_EXIST == 0:
            with open(config_file, 'a') as add_file:
                add_file.write(f'\nnum_logs = {NUM_LOGS_VALUE}\n')

        ret_restart, res_restart = subprocess.getstatusoutput('service auditd restart')
        if ret_restart != 0:
            logger.error(f'Failed to restart the auditd :{res_restart}')
            Display("- Set the audit log rotate...", "FAILED")
            return
        ACTION_RESULT = ''
        NUM_RESULT = ''
        with open(config_file, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                line_strip = line.strip()
                if line_strip == '' or line_strip.startswith('#'):
                    continue
                if re.match(r'max_log_file_action\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        ACTION_RESULT = temp[1].strip()
                if re.match(r'num_logs\s*=', line_strip, re.IGNORECASE):
                    temp = line_strip.split('=')
                    if len(temp) == 2:
                        NUM_RESULT = temp[1].strip()
        if ACTION_RESULT.upper() != ACTION_VALUE or NUM_RESULT != NUM_LOGS_VALUE:
            logger.info("the audit log rotate is not set correctly")
            Display("- Set the audit log rotate...", "FAILED")
        else:
            logger.info("the audit log rotate is set, checking ok")
            Display("- Set the audit log rotate...", "FINISHED")
    else:
        Display("- Skip set the audit log rotate due to config file...", "SKIPPING")
