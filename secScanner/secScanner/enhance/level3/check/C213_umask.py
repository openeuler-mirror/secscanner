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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C213_umask():
    InsertSection("check the file umask value ")
    UMASK_VAL = ''
    with open("/etc/profile", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.search('mask', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2:#check if there is only one number after umask
                    UMASK_VAL = temp[1] # umask 022 UMASK_VAL: 022

    if UMASK_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC213\n")
        logger.warning("WRN_C213: %s", WRN_C213)
        logger.warning("SUG_C213: %s", SUG_C213)
        Display("- No umask set...", "WARNING")
    elif UMASK_VAL < '027':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC213\n")
        logger.warning("WRN_C213: %s", WRN_C213)
        logger.warning("SUG_C213: %s", SUG_C213)
        Display("- Wrong umask set...", "WARNING")
    else:
        logger.info("Has right umask set, checking ok")
        Display("- Has right umask set...", "OK")
