# -*- coding: utf-8 -*-

import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0123_debugShell():
    InsertSection("Check the debug-shell server's status in your Linux System ")
    ret,res = subprocess.getstatusoutput('systemctl is-enabled debug-shell')
    if ret != 0 and res == 'disabled':
        logger.info(f'The status of debug-shell is {res}')
        Display(f"- Check the status of debug-shell is {res}...", "OK")
    else:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0123\n")
        logger.warning("WRN_C0123: %s", WRN_C0123)
        logger.warning("SUG_C0123: %s", SUG_C0123)
        Display(f"- Check the status of debug-shell is {res}...", "WARNING")