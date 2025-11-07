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
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S411_checkFtp():
    '''
    Function: Set remove ftp
    '''
    set_remove_ftp = seconf.get('level3', 'set_ftp_install')
    InsertSection("Remove the Ftp in your Linux System...")
    if set_remove_ftp == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q ftp')
        if ret != 0:
            Display("- No package for the ftp...", "SKIPPING")
        else:
            try:
                set_result,_ = subprocess.getstatusoutput('yum remove ftp -y')
            except Exception:
                os.system('dnf remove ftp')
                
            if set_result == 0:
                logger.info("Set remove the ftp, checking ok")
                Display("- Set remove the ftp...", "FINISHED")
            else:
                logger.warning("Set remove the ftp failed")
                Display("- Set remove the ftp...", "FAILED")
    else:
        Display("- Skip set remove the ftp...", "SKIPPING")
