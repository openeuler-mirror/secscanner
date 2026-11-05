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

def C03403_atcronconfig():
    '''
    Function: Check whether the at and cron config is right
    '''
    InsertSection("Check whether the at and cron config is right")
    # 1 crond enabled
    result = subprocess.run(['systemctl', 'is-enabled', 'crond'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr != 'enabled':
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03403\n")
        logger.warning("WRN_C03403_0%d: %s", 1, WRN_C03403_01)
        logger.warning("SUG_C03403_0%d: %s", 1, SUG_C03403_01)
        Display("- The cron daemon is not enabled...", "WARNING")
    else:
        logger.info("The cron daemon is enabled")
        Display("- Check whether the cron daemon is enabled...", "OK")
    # 2 owner and permission of crontab and cron dirs
    cron_paths = ["/etc/crontab", "/etc/cron.hourly", "/etc/cron.daily",
                  "/etc/cron.weekly", "/etc/cron.monthly", "/etc/cron.d"]
    unsafe = []
    for path in cron_paths:
        if os.path.exists(path):
            st = os.stat(path)
            if st.st_uid != 0 or st.st_gid != 0 or st.st_mode & 0o077:
                unsafe.append(path)
    if unsafe:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03403\n")
        logger.warning("WRN_C03403_0%d: %s", 2, WRN_C03403_02)
        logger.warning("SUG_C03403_0%d: %s", 2, SUG_C03403_02)
        Display("- Found unsafe owner or permission of crontab and cron dirs...", "WARNING")
    else:
        logger.info("Owner and permission of crontab and cron dirs are right")
        Display("- Check the owner and permission of crontab and cron dirs...", "OK")
    # 3 deny files should not exist
    deny_exists = [p for p in ("/etc/cron.deny", "/etc/at.deny") if os.path.exists(p)]
    if deny_exists:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03403\n")
        logger.warning("WRN_C03403_0%d: %s", 3, WRN_C03403_03)
        logger.warning("SUG_C03403_0%d: %s", 3, SUG_C03403_03)
        Display("- Found cron deny files...", "WARNING")
    else:
        logger.info("Cron deny files do not exist")
        Display("- Check whether the cron deny files exist...", "OK")
    # 4 allow files exist with right permission
    allow_bad = []
    for path in ("/etc/cron.allow", "/etc/at.allow"):
        if os.path.exists(path):
            st = os.stat(path)
            if st.st_uid != 0 or st.st_gid != 0 or (st.st_mode & 0o777) != 0o600:
                allow_bad.append(path)
        else:
            allow_bad.append(path)
    if allow_bad:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03403\n")
        logger.warning("WRN_C03403_0%d: %s", 4, WRN_C03403_04)
        logger.warning("SUG_C03403_0%d: %s", 4, SUG_C03403_04)
        Display("- The cron allow files do not exist or permission is not right...", "WARNING")
    else:
        logger.info("Cron allow files exist and permission are right")
        Display("- Check the cron allow files...", "OK")
