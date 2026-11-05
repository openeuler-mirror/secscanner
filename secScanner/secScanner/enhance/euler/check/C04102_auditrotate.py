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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C04102_auditrotate():
    '''
    Function: Check whether the audit log rotate is enabled in /etc/audit/auditd.conf
    '''
    InsertSection("Check the audit log rotate config in /etc/audit/auditd.conf")
    config_file = "/etc/audit/auditd.conf"
    if not os.path.exists(config_file):
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04102\n")
        logger.warning("WRN_C04102: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C04102: %s %s", config_file, SUG_no_file)
        Display(f"- {config_file} does not exist...", "SKIPPING")
        return
    MAX_LOG_FILE_ACTION_VAL = ''
    NUM_LOGS_VAL = ''
    with open(config_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            line_strip = line.strip()
            if line_strip == '' or line_strip.startswith('#'):
                continue
            if re.match('max_log_file_action', line_strip, re.IGNORECASE):
                temp = line_strip.split('=')
                if len(temp) == 2:
                    MAX_LOG_FILE_ACTION_VAL = temp[1].strip()
            if re.match('num_logs', line_strip, re.IGNORECASE):
                temp = line_strip.split('=')
                if len(temp) == 2:
                    NUM_LOGS_VAL = temp[1].strip()

    if MAX_LOG_FILE_ACTION_VAL.upper() not in ('ROTATE', 'KEEP_LOGS'):
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04102\n")
        logger.warning("WRN_C04102_01: %s", WRN_C04102_01)
        logger.warning("SUG_C04102_01: %s", SUG_C04102_01)
        Display("- The max_log_file_action of audit log rotate is not safe...", "WARNING")
    else:
        logger.info("The max_log_file_action of audit log rotate is safe, checking OK")
        Display("- Check the max_log_file_action of audit log rotate...", "OK")

    if not NUM_LOGS_VAL.isdigit() or not 2 <= int(NUM_LOGS_VAL) <= 99:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04102\n")
        logger.warning("WRN_C04102_02: %s", WRN_C04102_02)
        logger.warning("SUG_C04102_02: %s", SUG_C04102_02)
        Display("- The num_logs of audit log rotate is not safe...", "WARNING")
    else:
        logger.info("The num_logs of audit log rotate is safe, checking OK")
        Display("- Check the num_logs of audit log rotate...", "OK")
