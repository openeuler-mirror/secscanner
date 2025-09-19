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

def S0302_avoidWireless():
    InsertSection("Avoid using wireless network...")
    set_avoidWireless = seconf.get('euler', 'set_avoidWireless')
    if set_avoidWireless == 'yes':
        ret1, result1 = subprocess.getstatusoutput("nmcli radio all")
        if ret1 == 0:
            lines = result1.split("\n")
            status = lines[1].strip().split()
            if status[1].strip() in ["disabled", "已禁用"] and status[3].strip() in ["disabled", "已禁用"]:
                Display("- Checking wireless network is disabled", "FINISHED")
            else:
                ret2, result2 = subprocess.getstatusoutput("nmcli radio all off")
                if ret2 == 0:
                    ret3, result3 = subprocess.getstatusoutput("nmcli radio all")
                    if ret3 == 0:
                        lines = result3.split("\n")
                        status = lines[1].strip().split()
                        if status[1].strip() in ["disabled", "已禁用"] and status[3].strip() in ["disabled", "已禁用"]:
                            logger.info('Set wireless network ok...')
                            Display("- Set wireless network...", "FINISHED")
                        else:
                            logger.warning('Fail to disabled the wireless network')
                            Display("- Fail to disabled the wireless network", "FAILED")
                else:
                    logger.warning('Fail to disabled the wireless network')
                    Display("- Fail to disabled the wireless network", "FAILED")
    else:
        Display("- Skip set wireless network...", "SKIPPING")
