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

def C0128_checkYpserv():
    InsertSection("Check whether the ypserv software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q ypserv')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0128\n")
        logger.warning("WRN_C0128: %s", WRN_C0128)
        logger.warning("SUG_C0128: %s", SUG_C0128)
        Display(f"- Check the ypserv software is installed...", "WARNING")
    else:
        logger.info(f"The ypserv status is: {res}")
        Display(f"- Check the ypserv software is uninstall...", "OK")