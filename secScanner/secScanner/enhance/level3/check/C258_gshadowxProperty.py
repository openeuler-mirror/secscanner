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


def C258_gshadowxProperty():
    InsertSection("check /etc/gshadow- file property")
    filepath = '/etc/gshadow-'
    if os.path.exists(filepath):
        ret, result = subprocess.getstatusoutput(f'ls -al {filepath}')
        result = result.split()
        if ('----------' in result[0]):
            Display(f"- check if {filepath} property is 0 ...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC258\n")
                logger.warning("WRN_C258: %s", WRN_C258)
                logger.warning("SUG_C258: %s", SUG_C258)
                Display(f"- Check if {filepath} property is not 0...", "WARNING")
    else:
        Display(f"- file '/etc/gshadow-' does not exist...", "SKIPPED")
