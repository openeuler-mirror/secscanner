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

def C0138_nfsServer():
    InsertSection("Check whether the status of nfs-Server in your Linux System ")
    ret1,res1 = subprocess.getstatusoutput('rpm -q nfs-utils')
    if ret1 == 1:
        logger.info(f"{res1}")
        Display(f"- {res1}", "OK")
    else:
        ret,res= subprocess.getstatusoutput('systemctl is-enabled nfs-server')
        if ret == 0:
            with open(RESULT_FILE,'a+') as file:
                file.write("\nC0138\n")
            logger.warning("WRN_C0138: %s", WRN_C0138)
            logger.warning("SUG_C0138: %s", SUG_C0138)
            Display(f"- Check the nfs-Server is {res}...", "WARNING")
        else:
            logger.info(f"The nfs-Server status is: {res}")
            Display(f"- Check the nfs-Server is disabled...", "OK")
