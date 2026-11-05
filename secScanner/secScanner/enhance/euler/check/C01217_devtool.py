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

def C01217_devtool():
    '''
    Function: Check whether the development and compile tools are installed in your Linux System
    '''
    InsertSection("Check whether the development and compile tools are installed in your Linux System")
    devTools = ["gcc", "cpp", "mcpp", "flex", "cmake", "make", "rpm-build",
                "binutils-extra", "elfutils-extra", "llvm", "rpcgen", "gcc-c++", "libtool"]
    warnMessage = [WRN_C01217_01, WRN_C01217_02, WRN_C01217_03, WRN_C01217_04,
                   WRN_C01217_05, WRN_C01217_06, WRN_C01217_07, WRN_C01217_08,
                   WRN_C01217_09, WRN_C01217_10, WRN_C01217_11, WRN_C01217_12,
                   WRN_C01217_13]
    sugMessage = [SUG_C01217_01, SUG_C01217_02, SUG_C01217_03, SUG_C01217_04,
                  SUG_C01217_05, SUG_C01217_06, SUG_C01217_07, SUG_C01217_08,
                  SUG_C01217_09, SUG_C01217_10, SUG_C01217_11, SUG_C01217_12,
                  SUG_C01217_13]

    for i in range(len(devTools)):
        tool = devTools[i]
        ret, res = subprocess.getstatusoutput('rpm -q %s' % tool)
        if ret == 0:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01217\n")
            logger.warning("WRN_C01217_%02d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C01217_%02d: %s", (i + 1), sugMessage[i])
            Display(f"- Check the {tool} software is installed...", "WARNING")
        else:
            logger.info(f"The {tool} status is: {res}")
            Display(f"- Check the {tool} software is uninstall...", "OK")
