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
def C1021_histsize():
    InsertSection("check HISTSIZE of /etc/profile")
    HISTSIZE = '-1'
    config_file_path = "/etc/profile"
    config_file = "/etc/profile"
    if os.path.exists(config_file):
        with open(config_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not re.match(r'^\s*#', line):
                    if re.match(r'^\s*HISTSIZE\s*=', line):
                        HISTSIZE = line.split('=')[1].strip()
        HISTSIZE = int(HISTSIZE)
        if HISTSIZE >= 50 and HISTSIZE <= 100:
            logger.info("HISTSIZE set correctly, checking ok")
            Display("- Has set HISTSIZE correctly ...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC1021\n")
            logger.warning("WRN_C1021: %s", WRN_C1021)
            logger.warning("SUG_C1021: %s", SUG_C1021)
            Display("- Wrong HISTSIZE set...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC1021\n")
        logger.warning(f"WRN_C1021: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C1021: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
