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

def S0136_checkSamba():
    set_remove_Samba = seconf.get('euler', 'set_remove_Samba')
    InsertSection("Remove the samba in your Linux System...")
    if set_remove_Samba == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q samba')
        if ret != 0:
            logger.info(f'The status is:{res}')
            Display("- No package for the samba...", "SKIPPING")
        else:
            try:
                set_result,_= subprocess.getstatusoutput(' yum remove samba -y')
            except Exception:
                os.system('dnf remove samba -y')
                
            if set_result == 0:
                logger.info("Set remove the samba, checking ok")
                Display("- Set remove the samba...", "FINISHED")
            else:
                logger.warning("Set remove the samba failed")
                Display("- Set remove the samba...", "FAILED")
    else:
        Display("- Skip set remove the samba...", "SKIPPING")