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
import os
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0128_checkYpserv():
    set_remove_Ypserv = seconf.get('euler', 'set_remove_Ypserv')
    InsertSection("Remove the ypserv in your Linux System...")
    if set_remove_Ypserv == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q ypserv')
        if ret != 0:
            logger.info(f'The status is:{res}')
            Display("- No package for the ypserv...", "SKIPPING")
        else:
            try:
                set_result,_= subprocess.getstatusoutput(' yum remove ypserv -y')
            except Exception:
                os.system('dnf remove ypserv -y')
                
            if set_result == 0:
                logger.info("Set remove the ypserv, checking ok")
                Display("- Set remove the ypserv...", "FINISHED")
            else:
                logger.warning("Set remove the ypserv failed")
                Display("- Set remove the ypserv...", "FAILED")
    else:
        Display("- Skip set remove the ypserv...", "SKIPPING")