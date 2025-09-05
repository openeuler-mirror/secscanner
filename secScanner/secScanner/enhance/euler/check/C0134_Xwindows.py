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

def C0134_Xwindows():
    InsertSection("Check whether the Xwindows software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -qa xorg-x11*')
    if res !='':
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0134\n")
        logger.warning("WRN_C0134: %s", WRN_C0134)
        logger.warning("SUG_C0134: %s", SUG_C0134)
        Display(f"- Check the xorg-x11 software is installed...", "WARNING")
    else:
        logger.info(f"The xorg-x11 status is: {res}")
        Display(f"- Check the xorg-x11 software is uninstall...", "OK")
