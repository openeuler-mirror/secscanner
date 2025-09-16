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

def S0124_checkRsync():
    set_disable_Rsync = seconf.get('euler', 'set_disable_Rsync')
    InsertSection("Disabled the Rsyncd in your Linux System...")
    ret,res = subprocess.getstatusoutput('rpm -q rsync')
    if ret != 0:
        logger.info(f'{res}')
        Display(f"- Skip {res}...", "SKIPPING")
    else:
        if set_disable_Rsync == 'yes':
            ret1,res1 = subprocess.getstatusoutput('systemctl is-enabled rsyncd')
            if ret1 != 0:
                logger.info(f'The Status is {res1} of rsyncd')
                Display(f"-The Status is {res1} of rsyncd...", "SKIPPING")
            else:
                logger.warning(f'The Status is {res} of rsyncd')
                res2,_ = subprocess.getstatusoutput('systemctl --now disable rsyncd')
                if res2 != 0:
                    Display("- Set disbaled the rsyncd...", "FAILED")
                    raise ValueError("Failed to disbaled the rsyncd")
                Display("- Set disabled the rsyncd...", "FINISHED")
        else:
            Display("- Skip set disable the rsyncd...", "SKIPPING")
        