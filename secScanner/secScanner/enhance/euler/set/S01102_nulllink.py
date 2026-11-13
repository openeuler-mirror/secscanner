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

def S01102_nulllink():
    '''
    Function: Remove the null link files
    '''
    set_flag = seconf.get('euler', 'set_nulllink')
    InsertSection("Remove the null link files...")

    if set_flag == 'yes':
        ret, res = subprocess.getstatusoutput("find / -xdev -type l -follow 2>/dev/null")
        if ret == 0 and res.strip():
            set_result = True
            for path in res.strip().split('\n'):
                remove_result = subprocess.run(['rm', '-f', path], capture_output=True)
                if remove_result.returncode != 0:
                    set_result = False
                    logger.warning("Remove the null link file %s failed", path)
                else:
                    logger.info("Remove the null link file %s finished", path)
            if set_result:
                logger.info("Remove the null link files finished, checking ok")
                Display("- Remove the null link files...", "FINISHED")
            else:
                logger.warning("Remove the null link files failed")
                Display("- Remove the null link files...", "FAILED")
        else:
            logger.info("No null link file found")
            Display("- No null link file found...", "SKIPPING")
    else:
        Display("- Skip remove the null link files...", "SKIPPING")
