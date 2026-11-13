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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03504_smap():
    '''
    Function: Check whether the kernel SMAP is enabled
    '''
    InsertSection("Check whether the kernel SMAP is enabled")
    with open("/proc/cpuinfo", "r") as read_file:
        cpuStr = read_file.read()
    if "smap" in cpuStr.split():
        with open("/proc/cmdline", "r") as read_file:
            cmdStr = read_file.read()
        if re.search("nosmap", cmdStr, re.IGNORECASE):
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03504\n")
            logger.warning("WRN_C03504: %s", WRN_C03504)
            logger.warning("SUG_C03504: %s", SUG_C03504)
            Display("- The kernel SMAP is disabled by nosmap boot option...", "WARNING")
        else:
            logger.info("The kernel SMAP is enabled")
            Display("- Check whether the kernel SMAP is enabled...", "OK")
    else:
        logger.info("The CPU does not support SMAP, skip this check")
        Display("- The CPU does not support SMAP, skip this check...", "SKIPPING")
