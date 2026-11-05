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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03401_crontabscript():
    '''
    Function: Check whether the scripts in crontab are only writable by owner
    '''
    InsertSection("Check whether the crontab scripts are only writable by owner")
    crontab_file = "/etc/crontab"
    if os.path.exists(crontab_file):
        unsafe = False
        with open(crontab_file, "r") as read_file:
            for line in read_file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                fields = line.split()
                if len(fields) < 7:
                    continue
                cmd = fields[6]
                if not cmd.startswith('/'):
                    continue
                if os.path.isfile(cmd):
                    mode = os.stat(cmd).st_mode
                    if mode & 0o022:
                        unsafe = True
                        break
        if unsafe:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03401\n")
            logger.warning("WRN_C03401: %s", WRN_C03401)
            logger.warning("SUG_C03401: %s", SUG_C03401)
            Display("- Found crontab scripts writable by group or other...", "WARNING")
        else:
            logger.info("Crontab scripts are only writable by owner")
            Display("- Check whether the crontab scripts are only writable by owner...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03401\n")
        logger.warning(f"WRN_C03401: {crontab_file} {WRN_no_file}")
        logger.warning(f"SUG_C03401: {crontab_file} {SUG_no_file}")
        Display(f"- Config file: {crontab_file} not found...", "SKIPPING")
