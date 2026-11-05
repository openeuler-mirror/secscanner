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

def C01104_stickybit():
    '''
    Function: Check whether the world writable directories have the sticky bit set
    '''
    InsertSection("Check whether the world writable directories have the sticky bit set")
    ret, res = subprocess.getstatusoutput("find / -type d -perm -0002 -a ! -perm -1000 2>/dev/null")
    if ret == 0 and res.strip():
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01104\n")
        logger.warning("WRN_C01104: %s", WRN_C01104)
        logger.warning("SUG_C01104: %s", SUG_C01104)
        Display("- Found world writable directories without sticky bit set...", "WARNING")
    else:
        logger.info("All the world writable directories have the sticky bit set, checking ok")
        Display("- Check whether the world writable directories have the sticky bit set...", "OK")
