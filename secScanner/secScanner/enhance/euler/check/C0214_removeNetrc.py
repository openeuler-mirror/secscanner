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

def C0214_removeNetrc():
    InsertSection("Confirm the existence of the .netrc file in the Home directory")
    count = 0
    if os.path.exists('/etc/passwd'):
        ret, users = subprocess.getstatusoutput("grep -E -v '^(halt|sync|shutdown)' /etc/passwd")
        if ret == 0:
            users = [line.split(':') for line in users.strip().split('\n') if line.split(':')[6] not in ['/bin/false', '/sbin/nologin', '/usr/sbin/nologin']]
            for user in users:
                home = user[5]
                if os.path.isdir(home):
                    for root, dirs, files in os.walk(home):
                        if ".netrc" in files:
                            count += 1
            if count == 0:
                logger.info("Confirm the existence of the .netrc file in the Home directory, checking ok")
                Display("- check if the .netrc file in the Home directory...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0214\n")
                logger.warning("WRN_C0214_01: %s", WRN_C0214_01)
                logger.warning("SUG_C0214_01: %s", SUG_C0214_01)
                Display("- At least one .netrc file in the Home directory ...", "WARNING")

        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0214\n")
            logger.warning("WRN_C0214_02: %s", WRN_C0214_02)
            logger.warning("SUG_C0214_01: %s", SUG_C0214_01)
            Display("- Failed to obtain passwd user's home list ...", "WARNING")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0214\n")
        logger.warning("WRN_C0214_03: %s", WRN_C0214_03)
        logger.warning("SUG_C0214_02: %s", SUG_C0214_02)
        Display("- file /etc/passwd does not exist...", "WARNING")


