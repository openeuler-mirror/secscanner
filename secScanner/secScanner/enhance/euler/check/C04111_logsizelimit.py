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

def C04111_logsizelimit():
    '''
    Function: Check whether the audit log size limit is configured in /etc/audit/auditd.conf
    '''
    InsertSection("Check the audit log size limit config in /etc/audit/auditd.conf")
    config_file = "/etc/audit/auditd.conf"
    if not os.path.exists(config_file):
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04111\n")
        logger.warning("WRN_C04111: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C04111: %s %s", config_file, SUG_no_file)
        Display(f"- {config_file} does not exist...", "SKIPPING")
        return
    MAX_LOG_FILE_VAL = ''
    with open(config_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            line_strip = line.strip()
            if line_strip == '' or line_strip.startswith('#'):
                continue
            if re.match(r'max_log_file\s*=', line_strip, re.IGNORECASE):
                temp = line_strip.split('=')
                if len(temp) == 2:
                    MAX_LOG_FILE_VAL = temp[1].strip()

    if MAX_LOG_FILE_VAL == '' or not MAX_LOG_FILE_VAL.isdigit() or int(MAX_LOG_FILE_VAL) <= 0:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04111\n")
        logger.warning("WRN_C04111: %s", WRN_C04111)
        logger.warning("SUG_C04111: %s", SUG_C04111)
        Display("- The max_log_file of audit log size limit is not safe...", "WARNING")
    else:
        logger.info("The max_log_file of audit log size limit is safe, checking OK")
        Display("- Check the max_log_file of audit log size limit...", "OK")
