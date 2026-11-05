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

def C01216_debugtool():
    '''
    Function: Check whether the debug tools are installed in your Linux System
    '''
    InsertSection("Check whether the debug tools are installed in your Linux System")
    debugTools = ["strace", "gdb", "perf", "binutils-extra", "appict", "kmem_analyzer_tools"]
    warnMessage = [WRN_C01216_01, WRN_C01216_02, WRN_C01216_03, WRN_C01216_04,
                   WRN_C01216_05, WRN_C01216_06]
    sugMessage = [SUG_C01216_01, SUG_C01216_02, SUG_C01216_03, SUG_C01216_04,
                  SUG_C01216_05, SUG_C01216_06]

    for i in range(len(debugTools)):
        tool = debugTools[i]
        ret, res = subprocess.getstatusoutput('rpm -q %s' % tool)
        if ret == 0:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01216\n")
            logger.warning("WRN_C01216_%02d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C01216_%02d: %s", (i + 1), sugMessage[i])
            Display(f"- Check the {tool} software is installed...", "WARNING")
        else:
            logger.info(f"The {tool} status is: {res}")
            Display(f"- Check the {tool} software is uninstall...", "OK")
