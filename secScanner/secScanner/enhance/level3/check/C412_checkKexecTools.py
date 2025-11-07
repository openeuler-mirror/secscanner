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

def C412_checkKexecTools():
    InsertSection("Check whether the Kexec-tools software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q kexec-tools')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC412\n")
        logger.warning("WRN_C412: %s", WRN_C412)
        logger.warning("SUG_C412: %s", SUG_C412)
        Display(f"- Check the  Kexec-tools software is installed...", "WARNING")
    else:
        logger.info(f"The Kexec-tools status is: {res}")
        Display(f"- Check the Kexec-tools software is uninstall...", "OK")
