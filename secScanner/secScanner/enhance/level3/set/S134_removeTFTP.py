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

remove_tftp = seconf.get('level3', 'remove_tftp')

def S134_removeTFTP():
    InsertSection("remove installed tftp")
    if remove_tftp == 'yes':
        ret, result = subprocess.getstatusoutput('rpm -qa tftp*')
        if ret == 0 and result.strip():
            flag, output = subprocess.getstatusoutput('yum remove tftp -y')
            if flag == 0 and result.strip():
                logger.info("Successfully removed tftp...")
                Display("- Successfully removed tftp...", "FINISHED")
            else:
                logger.info("Failed to remove tftp...")
                Display("- Failed to remove tftp...", "FAILED")
        elif ret == 0 and not result.strip():
            logger.info("TFTP not installed...")
            Display("- TFTP not installed...", "SKIPPING")
        else:
            logger.info("Query command execution failed...")
            Display("- Query command execution failed...", "FAILED")
    else:
        Display("- Skip remove software tftp due to config file...", "SKIPPING")

