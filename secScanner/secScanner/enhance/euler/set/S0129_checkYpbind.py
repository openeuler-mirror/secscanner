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


import subprocess
import logging
import os
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0129_checkYpbind():
    '''
    Function: Set remove ypbind
    '''
    set_remove_ypbind = seconf.get('euler', 'set_remove_ypbind')
    InsertSection("Remove the ypbind in your Linux System...")
    if set_remove_ypbind == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q ypbind')
        if ret != 0:
            Display("- No package for the kexec-tools...", "SKIPPING")
        else:
            try:
                set_result,_=subprocess.getstatusoutput('yum remove ypbind -y')
            except Exception:
                os.system('dnf remove ypbind')
                
            if set_result == 0:
                logger.info("Set remove the ypbind, checking ok")
                Display("- Set remove the ypbind...", "FINISHED")
            else:
                logger.warning("Set remove the ypbind failed")
                Display("- Set remove the ypbind...", "FAILED")
    else:
        Display("- Skip set remove the ypbind...", "SKIPPING")
