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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0123_debugShell():
    set_disable_debugShell = seconf.get('euler', 'set_disable_debugShell')
    InsertSection("Disabled the debug-Shell in your Linux System...")
    if set_disable_debugShell == 'yes':
        ret,res = subprocess.getstatusoutput('systemctl is-enabled debug-shell')
        if ret != 0:
            logger.info(f'The Status is {res} of debug-shell')
            Display(f"-The Status is {res} of debug-shell...", "SKIPPING")
        else:
            logger.warning(f'The Status is {res} of debug-shell')
            res1,_ = subprocess.getstatusoutput('systemctl --now disable debug-shell')
            if res1 != 0:
                Display("- Set disbaled the debug-shell...", "FAILED")
                raise ValueError("Failed to disbaled the debug-shell")
            Display("- Set disabled the debug-shell...", "FINISHED")
    else:
        Display("- Skip set disable the debug-shell...", "SKIPPING")