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

def C421_nfsServer():
    InsertSection("Check whether the nfs-Server is enabled in your Linux System ")
    ret,res= subprocess.getstatusoutput('systemctl is-enabled nfs-server')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC421\n")
        logger.warning("WRN_C421: %s", WRN_C421)
        logger.warning("SUG_C421: %s", SUG_C421)
        Display(f"- Check the nfs-Server is enabled...", "WARNING")
    else:
        logger.info(f"The nfs-Server status is: {res}")
        Display(f"- Check the nfs-Server is disabled...", "OK")
