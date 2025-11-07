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


import os
import logging
from secScanner.commands.check_outprint import *
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

remove_http = seconf.get('level3', 'remove_http')

def S133_removehttp():
    InsertSection("remove installed http")
    if remove_http == 'yes':
        ret, result = subprocess.getstatusoutput('rpm -qa httpd*')
        if ret == 0 and result.strip():
            flag, output = subprocess.getstatusoutput('yum remove httpd -y')
            if flag == 0 and result.strip():
                logger.info("Successfully removed httpd...")
                Display("- Successfully removed httpd...", "FINISHED")
            else:
                logger.info("Failed to remove https...")
                Display("- Failed to remove https...", "FAILED")
        elif ret == 0 and not result.strip():
            logger.info("Http not installed...")
            Display("- Http not installed...", "SKIPPING")
        else:
            logger.info("Query command execution failed...")
            Display("- Query command execution failed...", "FAILED")
    else:
        Display("- Skip remove software http due to config file...", "SKIPPING")

