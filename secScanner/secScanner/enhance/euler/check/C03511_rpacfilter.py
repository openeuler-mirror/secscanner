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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03511_rpacfilter():
    '''
    Function: Check whether the reverse path filtering is enabled
    '''
    InsertSection("Check whether the reverse path filtering is enabled")
    rpParams = ["net.ipv4.conf.all.rp_filter",
                "net.ipv4.conf.default.rp_filter"]
    warnMessage = [WRN_C03511_01, WRN_C03511_02]
    sugMessage = [SUG_C03511_01, SUG_C03511_02]

    for i in range(len(rpParams)):
        param = rpParams[i]
        result = subprocess.run(['sysctl', param], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr[-1] != '1':
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03511\n")
            logger.warning("WRN_C03511_0%d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C03511_0%d: %s", (i + 1), sugMessage[i])
            Display("- %s is not set to 1..." % param, "WARNING")
        else:
            logger.info("Reverse path filtering parameter (%s) is set to 1", param)
            Display("- Check whether %s is set to 1..." % param, "OK")
