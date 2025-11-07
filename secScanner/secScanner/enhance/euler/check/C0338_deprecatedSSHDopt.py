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
def C0338_deprecatedSSHDopt():
    InsertSection("Check deprecated sshd options in sshd config file")
    ret, result = subprocess.getstatusoutput("sshd -t")
    if ret == 0 and result == '':
        logger.info("Check found 0 deprecated option of sshd")
        Display("- Check found 0 deprecated option of sshd", "OK")
    elif ret == 0 and "Deprecated option" in result:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0338\n")
        logger.warning("WRN_C0338_01: %s", WRN_C0338_01)
        logger.warning("SUG_C0338_01: %s", SUG_C0338_01)
        Display("- Found deprecated option of sshd...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0338\n")
        logger.warning("WRN_C0338_02: %s", WRN_C0338_02)
        logger.warning("SUG_C0338_02: %s", SUG_C0338_02)
        Display("- Error occured while excute sshd -t command...", "WARNING")
