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

def S01104_stickybit():
    '''
    Function: Set the sticky bit on the world writable directories
    '''
    set_flag = seconf.get('euler', 'set_stickybit')
    InsertSection("Set the sticky bit on the world writable directories...")

    if set_flag == 'yes':
        ret, res = subprocess.getstatusoutput("find / -type d -perm -0002 -a ! -perm -1000 2>/dev/null")
        if ret == 0 and res.strip():
            set_result = True
            for path in res.strip().split('\n'):
                chmod_result = subprocess.run(['chmod', '+t', path], capture_output=True)
                if chmod_result.returncode != 0:
                    set_result = False
                    logger.warning("Set the sticky bit on %s failed", path)
                else:
                    logger.info("Set the sticky bit on %s finished", path)
            if set_result:
                logger.info("Set the sticky bit on the world writable directories finished, checking ok")
                Display("- Set the sticky bit on the world writable directories...", "FINISHED")
            else:
                logger.warning("Set the sticky bit on the world writable directories failed")
                Display("- Set the sticky bit on the world writable directories...", "FAILED")
        else:
            logger.info("No world writable directory without sticky bit found")
            Display("- No world writable directory without sticky bit found...", "SKIPPING")
    else:
        Display("- Skip set the sticky bit on the world writable directories...", "SKIPPING")
