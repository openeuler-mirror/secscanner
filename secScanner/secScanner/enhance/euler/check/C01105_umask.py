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
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C01105_umask():
    '''
    Function: Check whether the UMASK config is right
    '''
    InsertSection("Check whether the UMASK config is right")
    config_file = "/etc/bashrc"
    umask_value = seconf.get('euler', 'umask_value')
    if os.path.exists(config_file):
        flag = False
        with open(config_file, 'r', encoding="utf-8") as read_file:
            lines = read_file.readlines()
            for line in lines:
                match = re.match(r'\s*umask\s+(\S+)', line)
                if match:
                    temp = match.group(1)
                    try:
                        if int(temp, 8) == int(umask_value, 8):
                            flag = True
                    except ValueError:
                        if temp == umask_value:
                            flag = True
        if flag:
            logger.info("The UMASK config is right, checking ok")
            Display("- Check whether the UMASK config is right...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01105\n")
            logger.warning("WRN_C01105: %s", WRN_C01105)
            logger.warning("SUG_C01105: %s", SUG_C01105)
            Display("- Check wrong set of UMASK...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01105\n")
        logger.warning("WRN_C01105: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C01105: %s %s", config_file, SUG_no_file)
        Display("- Config file: %s not found..." % config_file, "SKIPPING")
