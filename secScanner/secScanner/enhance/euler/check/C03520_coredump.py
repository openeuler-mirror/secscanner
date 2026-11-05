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
import subprocess
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03520_coredump():
    '''
    Function: Check whether the core dump config is right
    '''
    InsertSection("Check whether the core dump config is right")
    disabled = False
    result = subprocess.run("ulimit -c", shell=True, capture_output=True)
    ulimitStr = result.stdout.strip().decode("utf-8")
    if ulimitStr == '0':
        disabled = True
    limits_file = "/etc/security/limits.conf"
    if not disabled and os.path.exists(limits_file):
        with open(limits_file, "r") as read_file:
            for line in read_file:
                if re.match(r"\s*\*\s+hard\s+core\s+0\b", line):
                    disabled = True
                    break
    if disabled:
        logger.info("Core dump is disabled")
        Display("- Check whether the core dump config is right...", "OK")
    else:
        limited = False
        result_pattern = subprocess.run(['sysctl', 'kernel.core_pattern'], capture_output=True)
        patternStr = result_pattern.stdout.strip().decode("utf-8")
        core_path = re.sub(r"^\s*kernel\.core_pattern\s*=\s*", "", patternStr)
        if re.match(r"^/.+", core_path):
            core_dir = os.path.dirname(core_path)
            if os.path.isdir(core_dir):
                rights_digit = oct(os.stat(core_dir).st_mode & 0o7777)[2:]
                if rights_digit in ('700', '1770', '1777'):
                    limited = True
        if limited:
            logger.info("Core dump path is limited safely")
            Display("- Check whether the core dump config is right...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03520\n")
            logger.warning("WRN_C03520: %s", WRN_C03520)
            logger.warning("SUG_C03520: %s", SUG_C03520)
            Display("- The core dump config is not safe...", "WARNING")
