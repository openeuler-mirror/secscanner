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

def C02408_suenv():
    '''
    Function: check that su command does not inherit the user PATH environment variable
    '''
    InsertSection("check that su command does not inherit the user PATH environment variable")
    config_file = "/etc/login.defs"
    if os.path.exists(config_file):
        always_set_path = 'unset'
        with open(config_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match(r'\s*ALWAYS_SET_PATH\b', line) and not re.match(r'\s*#', line):
                    always_set_path = 'wrong'
                    if re.search(r'yes', line, re.IGNORECASE):
                        always_set_path = 'right'
        if always_set_path == 'right':
            logger.info("ALWAYS_SET_PATH is set to yes in /etc/login.defs, checking ok")
            Display("- Has ALWAYS_SET_PATH set to yes in /etc/login.defs...", "OK")
        elif always_set_path == 'unset':
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02408\n")
            logger.warning("WRN_C02408_01: %s", WRN_C02408_01)
            logger.warning("SUG_C02408: %s", SUG_C02408)
            Display("- No ALWAYS_SET_PATH config set in /etc/login.defs...", "WARNING")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02408\n")
            logger.warning("WRN_C02408_02: %s", WRN_C02408_02)
            logger.warning("SUG_C02408: %s", SUG_C02408)
            Display("- ALWAYS_SET_PATH is not set to yes in /etc/login.defs...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02408\n")
        logger.warning(f"WRN_C02408: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C02408: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")

