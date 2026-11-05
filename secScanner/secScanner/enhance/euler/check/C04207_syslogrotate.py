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

def C04207_syslogrotate():
    '''
    Function: Check whether the rsyslog log rotate is configured in /etc/logrotate.d/rsyslog
    '''
    InsertSection("Check the rsyslog log rotate config in /etc/logrotate.d/rsyslog")
    config_file = "/etc/logrotate.d/rsyslog"
    if not os.path.exists(config_file):
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04207\n")
        logger.warning("WRN_C04207: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C04207: %s %s", config_file, SUG_no_file)
        Display(f"- {config_file} does not exist...", "SKIPPING")
        return
    log_paths = ["/var/log/cron", "/var/log/maillog", "/var/log/messages", "/var/log/secure", "/var/log/spooler"]
    rotate_params = ["maxage", "rotate", "compress", "size"]
    with open(config_file, "r") as file:
        content = file.read()

    missing_paths = [log_path for log_path in log_paths if log_path not in content]
    missing_params = [rotate_param for rotate_param in rotate_params if not re.search(rf'^\s*{rotate_param}\b', content, re.MULTILINE)]

    if missing_paths:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04207\n")
        logger.warning("WRN_C04207_01: %s", WRN_C04207_01)
        logger.warning("SUG_C04207_01: %s", SUG_C04207_01)
        Display(f"- The rsyslog log rotate paths {missing_paths} are not configured...", "WARNING")
    else:
        logger.info("The rsyslog log rotate paths are configured, checking OK")
        Display("- Check the rsyslog log rotate paths config...", "OK")

    if missing_params:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04207\n")
        logger.warning("WRN_C04207_02: %s", WRN_C04207_02)
        logger.warning("SUG_C04207_02: %s", SUG_C04207_02)
        Display(f"- The rsyslog log rotate params {missing_params} are not configured...", "WARNING")
    else:
        logger.info("The rsyslog log rotate params are configured, checking OK")
        Display("- Check the rsyslog log rotate params config...", "OK")
