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

def S03402_cronDaemon():
    '''
    Function: Set the cron daemon enabled
    '''
    InsertSection("Set the cron daemon enabled...")
    set_cronDaemon = seconf.get('euler', 'set_cronDaemon')
    if set_cronDaemon == 'yes':
        result = subprocess.run(['systemctl', 'is-enabled', 'crond'], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr == 'enabled':
            logger.info("The cron daemon already enabled")
            Display("- The cron daemon has already been enabled...", "SKIPPING")
        else:
            ret, output = subprocess.getstatusoutput('systemctl --now enable crond')
            if ret == 0:
                logger.info("Enable the cron daemon finish")
                Display("- Enable the cron daemon...", "FINISHED")
            else:
                logger.warning("Enable the cron daemon failed")
                Display("- Enable the cron daemon...", "FAILED")
    else:
        Display("- Skip enable the cron daemon due to config file...", "SKIPPING")
