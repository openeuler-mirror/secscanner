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

def S412_checkKexecTools():
    '''
    Function: Set remove kexec-tools
    '''
    set_remove_kexec = seconf.get('level3', 'set_kexec-tools_install')
    InsertSection("Remove the kexec-tools in your Linux System...")
    if set_remove_kexec == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q kexec-tools')
        if ret != 0:
            Display("- No package for the kexec-tools...", "SKIPPING")
        else:
            try:
                set_result,_=subprocess.getstatusoutput('yum remove kexec-tools -y')
            except Exception:
                os.system('dnf remove kexec-tools')
                
            if set_result == 0:
                logger.info("Set remove the kexec-tools, checking ok")
                Display("- Set remove the kexec-tools...", "FINISHED")
            else:
                logger.warning("Set remove the kexec-tools failed")
                Display("- Set remove the kexec-tools...", "FAILED")
    else:
        Display("- Skip set remove the kexec-tools...", "SKIPPING")
