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

def C01101_nouserfiles():
    '''
    Function: Check whether there are files or directories without owner or group
    '''
    InsertSection("Check whether there are files or directories without owner or group")
    findTypes = ["nouser", "nogroup"]
    warnMessage = [WRN_C01101_01, WRN_C01101_02]
    sugMessage = [SUG_C01101_01, SUG_C01101_02]

    for i in range(len(findTypes)):
        findType = findTypes[i]
        cmd = "find `df -l | sed -n '2,$p' | awk '{print $6}'` -xdev -%s 2>/dev/null" % findType
        ret, res = subprocess.getstatusoutput(cmd)
        if ret == 0 and res.strip():
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01101\n")
            logger.warning("WRN_C01101_%02d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C01101_%02d: %s", (i + 1), sugMessage[i])
            Display("- Found files or directories without %s..." % findType, "WARNING")
        else:
            logger.info("No file or directory without %s found, checking ok", findType)
            Display("- Check whether files or directories without %s exist..." % findType, "OK")
