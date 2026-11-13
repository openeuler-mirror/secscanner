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

def C01115_openfiles():
    '''
    Function: Check whether the open file limits of users are set correctly
    '''
    InsertSection("Check whether the open file limits of users are set correctly")

    ret1, res1 = subprocess.getstatusoutput('ulimit -Sn')
    ret2, res2 = subprocess.getstatusoutput('ulimit -Hn')
    if ret1 == 0 and ret2 == 0 and res1.strip().isdigit() and res2.strip().isdigit():
        soft_limit = int(res1.strip())
        hard_limit = int(res2.strip())
        if soft_limit > 0 and soft_limit <= hard_limit:
            logger.info("The open file limits of the session are right, checking ok")
            Display("- Check the open file limits of the session...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01115\n")
            logger.warning("WRN_C01115_01: %s", WRN_C01115_01)
            logger.warning("SUG_C01115_01: %s", SUG_C01115_01)
            Display("- Check wrong set of the open file limits of the session...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01115\n")
        logger.warning("WRN_C01115_01: %s", WRN_C01115_01)
        logger.warning("SUG_C01115_01: %s", SUG_C01115_01)
        Display("- Failed to get the open file limits of the session...", "WARNING")

    config_file = '/etc/security/limits.conf'
    if os.path.exists(config_file):
        wrong_flag = False
        soft_limits = {}
        hard_limits = {}
        with open(config_file, 'r', encoding="utf-8") as read_file:
            lines = read_file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            fields = line.split()
            if len(fields) >= 4 and fields[2] == 'nofile':
                if fields[1] == 'soft' and fields[3].isdigit():
                    soft_limits[fields[0]] = int(fields[3])
                if fields[1] == 'hard' and fields[3].isdigit():
                    hard_limits[fields[0]] = int(fields[3])
        for domain, soft_value in soft_limits.items():
            if domain in hard_limits and soft_value > hard_limits[domain]:
                wrong_flag = True
        if wrong_flag:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01115\n")
            logger.warning("WRN_C01115_02: %s", WRN_C01115_02)
            logger.warning("SUG_C01115_02: %s", SUG_C01115_02)
            Display("- Check wrong set of nofile limits in limits.conf...", "WARNING")
        else:
            logger.info("The nofile limits in limits.conf are right, checking ok")
            Display("- Check the nofile limits in limits.conf...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01115\n")
        logger.warning("WRN_C01115_02: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C01115_02: %s %s", config_file, SUG_no_file)
        Display("- Config file: %s not found..." % config_file, "SKIPPING")
