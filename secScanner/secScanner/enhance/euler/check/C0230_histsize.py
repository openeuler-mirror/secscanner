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

def C0230_histsize():
    InsertSection("check HISTSIZE of /etc/profile")
    HISTSIZE = ''
    config_file_path = "/etc/profile"
    with open(config_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not re.match(r'^\s*#', line):
                if re.match(r'^\s*HISTSIZE\s*=', line):
                    HISTSIZE = line.split('=')[1].strip()
                    break
    HISTSIZE = int(HISTSIZE)
    if HISTSIZE >= 50 and HISTSIZE <= 100:
        logger.info("HISTSIZE set correctly, checking ok")
        Display("- Has set HISTSIZE correctly ...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0230\n")
        logger.warning("WRN_C0230: %s", WRN_C0230)
        logger.warning("SUG_C0230: %s", SUG_C0230)
        Display("- Wrong HISTSIZE set...", "WARNING")
