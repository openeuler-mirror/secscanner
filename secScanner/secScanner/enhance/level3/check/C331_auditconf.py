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
'''
max_log_file_action=$(grep -q '^\s*max_log_file_action\s*=' "$auditd_conf" &&
grep '^\s*max_log_file_action\s*=' "$auditd_conf" | sed
's/^[[:space:]]*max_log_file_action[[:space:]]*=[[:space:]]*//')
'''

def C331_auditconf():
    InsertSection("check the config of audit.conf")
    config_file = "/etc/audit/auditd.conf"
    if os.path.exists(config_file):
        max_log_file_action = ''
        config_file_path = "/etc/audit/auditd.conf"
        with open(config_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not re.match(r'^\s*#', line):
                    if re.match(r'^\s*max_log_file_action\s*=', line):
                        max_log_file_action = line.split('=')[1].strip()
                        break
        if max_log_file_action == "keep_logs":
            logger.info("audit.conf set correctly, checking ok")
            Display("- Has set audit.conf correctly ...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC331\n")
            logger.warning("WRN_C331: %s", WRN_C331)
            logger.warning("SUG_C331: %s", SUG_C331)
            Display("- Wrong audit.conf set...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC331\n")
        logger.warning(f"WRN_C331: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C331: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")


