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

def S0138_nfsServer():
    '''
    Function: Set disabled the Nfs-server
    '''
    set_disabled_NfsServer = seconf.get('euler', 'set_disabled_NfsServer')
    InsertSection("Disabled the Nfs-server in your Linux System...")
    if set_disabled_NfsServer == 'yes':
        ret1,res1 = subprocess.getstatusoutput('rpm -q nfs-utils')
        if ret1 == 1:
            logger.info(f"{res1}")
            Display(f"- {res1}", "SKIPPING")
        else:
            ret,res= subprocess.getstatusoutput('systemctl is-enabled nfs-server')
            if ret != 0:
                logger.info(f'The Status is {res} of Nfs-server')
                Display(f"-The Status is {res} of Nfs-server...", "SKIPPING")
            else:
                logger.warning(f'The Status is {res} of Nfs-server')
                res2 = os.system('systemctl disable nfs-server')
                if res2 != 0:
                    Display("- Set disbaled the Nfs-server...", "FAILED")
                    raise ValueError("Failed to disbaled the nfs-server")
                Display("- Set disabled the Nfs-server...", "FINISHED")
    else:
        Display("- Skip set disabled the Nfs-server...", "SKIPPING")
