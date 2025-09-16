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

def S0127_checkCups():
    set_remove_Cups = seconf.get('euler', 'set_remove_Cups')
    InsertSection("Remove the Cups in your Linux System...")
    if set_remove_Cups == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q cups')
        if ret != 0:
            logger.info(f'The status is:{res}')
            Display("- No package for the cups...", "SKIPPING")
        else:
            try:
                set_result,_= subprocess.getstatusoutput(' yum remove cups -y')
            except Exception:
                os.system('dnf remove cups -y')
                
            if set_result == 0:
                logger.info("Set remove the Cups, checking ok")
                Display("- Set remove the Cups...", "FINISHED")
            else:
                logger.warning("Set remove the Cups failed")
                Display("- Set remove the Cups...", "FAILED")
    else:
        Display("- Skip set remove the Cups...", "SKIPPING")