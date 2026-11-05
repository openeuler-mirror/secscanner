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
import os
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C01103_hiddenexec():
    '''
    Function: Check whether there are hidden executable files
    '''
    InsertSection("Check whether there are hidden executable files")
    except_files = ['.bashrc', '.bash_profile', '.bash_logout']
    hidden_exec_files = []
    ret, res = subprocess.getstatusoutput("find / -type f -name '\\.*' -perm /+x 2>/dev/null")
    if ret == 0 and res.strip():
        for line in res.strip().split('\n'):
            if os.path.basename(line) not in except_files:
                hidden_exec_files.append(line)
    if hidden_exec_files:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01103\n")
        logger.warning("WRN_C01103: %s", WRN_C01103)
        logger.warning("SUG_C01103: %s", SUG_C01103)
        Display("- Found hidden executable files in your Linux System...", "WARNING")
    else:
        logger.info("No hidden executable file found, checking ok")
        Display("- Check whether hidden executable files exist...", "OK")
