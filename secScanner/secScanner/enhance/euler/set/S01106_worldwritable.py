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

def S01106_worldwritable():
    '''
    Function: Remove the world writable permission of the files
    '''
    set_flag = seconf.get('euler', 'set_worldwritable')
    InsertSection("Remove the world writable permission of the files...")

    if set_flag == 'yes':
        ret, res = subprocess.getstatusoutput("find / -path /proc -prune -o -path /sys -prune -o -type f -perm -0002 2>/dev/null")
        if ret == 0 and res.strip():
            set_result = True
            for path in res.strip().split('\n'):
                chmod_result = subprocess.run(['chmod', 'o-w', path], capture_output=True)
                if chmod_result.returncode != 0:
                    set_result = False
                    logger.warning("Remove the world writable permission of %s failed", path)
                else:
                    logger.info("Remove the world writable permission of %s finished", path)
            if set_result:
                logger.info("Remove the world writable permission of the files finished, checking ok")
                Display("- Remove the world writable permission of the files...", "FINISHED")
            else:
                logger.warning("Remove the world writable permission of the files failed")
                Display("- Remove the world writable permission of the files...", "FAILED")
        else:
            logger.info("No world writable file found")
            Display("- No world writable file found...", "SKIPPING")
    else:
        Display("- Skip remove the world writable permission of the files...", "SKIPPING")
