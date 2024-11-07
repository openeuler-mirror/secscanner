# -*- coding: utf-8 -*-

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
            with open(RESULT_FILE,'a+') as file:
                file.write("\nC0124\n")
            logger.warning("WRN_C0124: %s", WRN_C0124)
            logger.warning("SUG_C0124: %s", SUG_C0124)
            Display(f"- Check the status of rsyncd is {res1}...", "WARNING")