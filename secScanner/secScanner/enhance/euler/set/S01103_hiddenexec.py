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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01103_hiddenexec():
    '''
    Function: Remove the executable permission of the hidden executable files
    '''
    set_flag = seconf.get('euler', 'set_hiddenexec')
    InsertSection("Remove the executable permission of the hidden executable files...")

    if set_flag == 'yes':
        except_files = ['.bashrc', '.bash_profile', '.bash_logout']
        hidden_exec_files = []
        ret, res = subprocess.getstatusoutput("find / -type f -name '\\.*' -perm /+x 2>/dev/null")
        if ret == 0 and res.strip():
            for line in res.strip().split('\n'):
                if os.path.basename(line) not in except_files:
                    hidden_exec_files.append(line)
        if hidden_exec_files:
            set_result = True
            for path in hidden_exec_files:
                chmod_result = subprocess.run(['chmod', '644', path], capture_output=True)
                if chmod_result.returncode != 0:
                    set_result = False
                    logger.warning("Remove the executable permission of %s failed", path)
                else:
                    logger.info("Remove the executable permission of %s finished", path)
            if set_result:
                logger.info("Remove the executable permission of the hidden executable files finished, checking ok")
                Display("- Remove the executable permission of the hidden executable files...", "FINISHED")
            else:
                logger.warning("Remove the executable permission of the hidden executable files failed")
                Display("- Remove the executable permission of the hidden executable files...", "FAILED")
        else:
            logger.info("No hidden executable file found")
            Display("- No hidden executable file found...", "SKIPPING")
    else:
        Display("- Skip remove the executable permission of the hidden executable files...", "SKIPPING")
