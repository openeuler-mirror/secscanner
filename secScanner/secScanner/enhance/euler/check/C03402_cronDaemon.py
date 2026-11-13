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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03402_cronDaemon():
    '''
    Function: Check whether the cron daemon is enabled
    '''
    InsertSection("Check whether the cron daemon is enabled")
    result = subprocess.run(['systemctl', 'is-enabled', 'crond'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr != 'enabled':
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03402\n")
        logger.warning("WRN_C03402: %s", WRN_C03402)
        logger.warning("SUG_C03402: %s", SUG_C03402)
        Display("- The cron daemon is not enabled...", "WARNING")
    else:
        logger.info("The cron daemon is enabled")
        Display("- Check whether the cron daemon is enabled...", "OK")
