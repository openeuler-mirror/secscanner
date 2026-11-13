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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S03401_crontabscript():
    '''
    Function: Set the crontab scripts only writable by owner
    '''
    InsertSection("Set the crontab scripts only writable by owner...")
    set_crontabscript = seconf.get('euler', 'set_crontabscript')
    if set_crontabscript == 'yes':
        crontab_file = "/etc/crontab"
        if os.path.exists(crontab_file):
            fixed = 0
            failed = 0
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
                            try:
                                os.chmod(cmd, mode & ~0o022)
                                fixed += 1
                            except Exception:
                                failed += 1
            if failed:
                logger.warning("Set crontab scripts writable permission failed")
                Display("- Set the crontab scripts only writable by owner...", "FAILED")
            elif fixed:
                logger.info("Set crontab scripts only writable by owner finish")
                Display("- Set the crontab scripts only writable by owner...", "FINISHED")
            else:
                logger.info("Crontab scripts already only writable by owner")
                Display("- Crontab scripts already only writable by owner...", "SKIPPING")
        else:
            logger.warning("crontab config file not exist")
            Display("- crontab config file not exist...", "FAILED")
    else:
        Display("- Skip set the crontab scripts writable permission due to config file...", "SKIPPING")
