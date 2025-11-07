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
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C251_passwdProperty():
    InsertSection("check /etc/passwd file property")
    filepath = '/etc/passwd'
    if os.path.exists(filepath):
        ret, result = subprocess.getstatusoutput(f'ls -al {filepath}')
        result = result.split()
        if ('-rw-r--r--' in result[0]):
            Display(f"- check if {filepath} property is 644 ...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC251\n")
                logger.warning("WRN_C251: %s", WRN_C251)
                logger.warning("SUG_C251: %s", SUG_C251)
                Display(f"- Check if {filepath} property is not 644...", "WARNING")
    else:
        Display(f"- file '/etc/passwd' does not exist...", "SKIPPED")
