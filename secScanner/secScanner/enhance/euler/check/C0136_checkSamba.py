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

def C0135_checkHttpd():
    InsertSection("Check whether the httpd software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q httpd')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0135\n")
        logger.warning("WRN_C0135: %s", WRN_C0135)
        logger.warning("SUG_C0135: %s", SUG_C0135)
        Display(f"- Check the httpd software is installed...", "WARNING")
    else:
        logger.info(f"The httpd status is: {res}")
        Display(f"- Check the httpd software is uninstall...", "OK")