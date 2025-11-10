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

def C112_UIDunique():
    InsertSection("Check if UID is unique")
    if os.path.exists('/etc/passwd'):
        duplicate_uids_found = False
        command = "cut -f3 -d: /etc/passwd | sort -n | uniq -c"
        ret, result = subprocess.getstatusoutput(command)
        if ret == 0:
            lines = result.split('\n')
            for line in lines:
                if not line.strip():
                    continue
                count, uid = line.strip().split()
                if int(count) > 1:
                    users_command = f"awk -F: '$3 == \"{uid}\" {{ print $1 }}' /etc/passwd"
                    ret, result = subprocess.getstatusoutput(users_command)
                    if ret == 0:
                        users = result.strip().split('\n')
                        duplicate_uids_found = True
                        with open(RESULT_FILE, "a") as file:
                            file.write("\nC112\n")
                        logger.warning("WRN_C112_01: %s", WRN_C112_01)
                        logger.warning("SUG_C112_01: %s", SUG_C112_01)
                        Display(f"- Duplicate UID ({uid}): {' '.join(users)}...", "WARNING")
                    else:
                        with open(RESULT_FILE, "a") as file:
                            file.write("\nC112\n")
                        logger.warning("WRN_C112_02: %s", WRN_C112_02)
                        logger.warning("SUG_C112_02: %s", SUG_C112_02)
                        Display("- Failed to retrieve users for UID...", "WARNING")
                        return
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC112\n")
            logger.warning("WRN_C112_03: %s", WRN_C112_03)
            logger.warning("SUG_C112_03: %s", SUG_C112_03)
            Display("- Failed to retrieve UID information...", "WARNING")
            return
        
        if not duplicate_uids_found:
            logger.info("Confirm UID uniqueness, checking OK")
            Display("- Confirm UID uniqueness...", "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC112\n")
        logger.warning("WRN_C112_04: %s", WRN_C112_04)
        logger.warning("SUG_C112_04: %s", SUG_C112_04)
        Display("- file /etc/passwd dose not exist...", "WARNING")
