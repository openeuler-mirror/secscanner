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

def S03403_atcronconfig():
    '''
    Function: Set the at and cron config right
    '''
    InsertSection("Set the at and cron config right...")
    set_atcronconfig = seconf.get('euler', 'set_atcronconfig')
    if set_atcronconfig == 'yes':
        # 1 enable crond
        result = subprocess.run(['systemctl', 'is-enabled', 'crond'], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr == 'enabled':
            logger.info("The cron daemon already enabled")
            Display("- The cron daemon has already been enabled...", "SKIPPING")
        else:
            ret, output = subprocess.getstatusoutput('systemctl --now enable crond')
            if ret == 0:
                logger.info("Enable the cron daemon finish")
                Display("- Enable the cron daemon...", "FINISHED")
            else:
                logger.warning("Enable the cron daemon failed")
                Display("- Enable the cron daemon...", "FAILED")
        # 2 crontab and cron dirs owner/permission
        cron_paths = ["/etc/crontab", "/etc/cron.hourly", "/etc/cron.daily",
                      "/etc/cron.weekly", "/etc/cron.monthly", "/etc/cron.d"]
        for path in cron_paths:
            if os.path.exists(path):
                st = os.stat(path)
                if st.st_uid != 0 or st.st_gid != 0 or st.st_mode & 0o077:
                    os.chown(path, 0, 0)
                    os.chmod(path, st.st_mode & ~0o077)
                    logger.info("Set owner and permission of %s finish", path)
                else:
                    logger.info("Owner and permission of %s already right", path)
        # 3 remove deny files
        for path in ("/etc/cron.deny", "/etc/at.deny"):
            if os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info("Remove %s finish", path)
                except Exception:
                    logger.warning("Remove %s failed", path)
            else:
                logger.info("%s does not exist", path)
        # 4 create allow files with right permission
        for path in ("/etc/cron.allow", "/etc/at.allow"):
            if not os.path.exists(path):
                with open(path, "w"):
                    pass
                logger.info("Create %s finish", path)
            else:
                logger.info("%s already exists", path)
            os.chown(path, 0, 0)
            os.chmod(path, 0o600)
        logger.info("Set at and cron config finish")
        Display("- Set the at and cron config...", "FINISHED")
    else:
        Display("- Skip set the at and cron config due to config file...", "SKIPPING")
