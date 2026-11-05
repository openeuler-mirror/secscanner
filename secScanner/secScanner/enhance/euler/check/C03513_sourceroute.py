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

def C03513_sourceroute():
    '''
    Function: Check whether the IP source routing is disabled
    '''
    InsertSection("Check whether the IP source routing is disabled")
    routeParams = ["net.ipv4.conf.all.accept_source_route",
                   "net.ipv4.conf.default.accept_source_route",
                   "net.ipv6.conf.all.accept_source_route",
                   "net.ipv6.conf.default.accept_source_route"]
    warnMessage = [WRN_C03513_01, WRN_C03513_02, WRN_C03513_03, WRN_C03513_04]
    sugMessage = [SUG_C03513_01, SUG_C03513_02, SUG_C03513_03, SUG_C03513_04]

    for i in range(len(routeParams)):
        param = routeParams[i]
        result = subprocess.run(['sysctl', param], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr[-1] != '0':
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03513\n")
            logger.warning("WRN_C03513_0%d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C03513_0%d: %s", (i + 1), sugMessage[i])
            Display("- %s is not set to 0..." % param, "WARNING")
        else:
            logger.info("IP source route parameter (%s) is set to 0", param)
            Display("- Check whether %s is set to 0..." % param, "OK")
