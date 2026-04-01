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

def C0124_checkRsync():
    InsertSection("Check the rsyncd server's status in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q rsync')
    if ret != 0:
        logger.info(f'The status of Rsync is :{res}')
        Display(f"-The Status is {res} of Rsync...", "OK")
    else:
        logger.info(f'The status of Rsync is :{res}')
        #check whether the server status
        ret1,res1 = subprocess.getstatusoutput('systemctl is-enabled rsyncd')
        if ret1 != 0 and res1 == 'disabled':
            logger.info(f'The status of rsyncd is {res1}')
            Display(f"- Check the status of rsyncd is {res1}...", "OK") 
        else:
            with open(RESULT_FILE,'a+', encoding="utf-8") as file:
                file.write("\nC0124\n")
            logger.warning("WRN_C0124: %s", WRN_C0124)
            logger.warning("SUG_C0124: %s", SUG_C0124)
            Display(f"- Check the status of rsyncd is {res1}...", "WARNING")
