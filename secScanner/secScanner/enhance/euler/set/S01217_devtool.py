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

def S01217_devtool():
    '''
    Function: Remove the development and compile tools in your Linux System
    '''
    set_remove_devtool = seconf.get('euler', 'set_devtool')
    InsertSection("Remove the development and compile tools in your Linux System...")
    if set_remove_devtool == 'yes':
        devTools = ["gcc", "cpp", "mcpp", "flex", "cmake", "make", "rpm-build",
                    "binutils-extra", "elfutils-extra", "llvm", "rpcgen", "gcc-c++", "libtool"]
        installed_tools = []
        for tool in devTools:
            ret, _ = subprocess.getstatusoutput('rpm -q %s' % tool)
            if ret == 0:
                installed_tools.append(tool)
        if not installed_tools:
            logger.info("No package for the development and compile tools")
            Display("- No package for the development and compile tools...", "SKIPPING")
        else:
            failed_tools = []
            for tool in installed_tools:
                try:
                    set_result, _ = subprocess.getstatusoutput('rpm -e %s' % tool)
                except Exception:
                    set_result = 1
                if set_result == 0:
                    logger.info(f"Set remove the {tool}, checking ok")
                else:
                    logger.warning(f"Failed to remove the {tool}")
                    failed_tools.append(tool)
            if failed_tools:
                logger.warning(f"Set remove the development and compile tools failed: {failed_tools}")
                Display("- Set remove the development and compile tools...", "FAILED")
            else:
                logger.info("Set remove the development and compile tools, checking ok")
                Display("- Set remove the development and compile tools...", "FINISHED")
    else:
        Display("- Skip set remove the development and compile tools...", "SKIPPING")
