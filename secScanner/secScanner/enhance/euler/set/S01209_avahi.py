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

def S01209_avahi():
    '''
    Function: Remove the avahi in your Linux System
    '''
    set_remove_avahi = seconf.get('euler', 'set_avahi')
    InsertSection("Remove the avahi in your Linux System...")
    if set_remove_avahi == 'yes':
        ret, res = subprocess.getstatusoutput('rpm -q avahi')
        if ret != 0:
            logger.info(f'The status is:{res}')
            Display("- No package for the avahi...", "SKIPPING")
        else:
            try:
                set_result, _ = subprocess.getstatusoutput('yum remove avahi -y')
            except Exception:
                os.system('dnf remove avahi -y')

            if set_result == 0:
                logger.info("Set remove the avahi, checking ok")
                Display("- Set remove the avahi...", "FINISHED")
            else:
                disable_result = os.system('systemctl --now disable avahi-daemon')
                if disable_result == 0:
                    logger.info("Failed to remove the avahi, set disabled the avahi-daemon instead")
                    Display("- Set disabled the avahi-daemon instead...", "FINISHED")
                else:
                    logger.warning("Set remove the avahi failed")
                    Display("- Set remove the avahi...", "FAILED")
    else:
        Display("- Skip set remove the avahi...", "SKIPPING")
