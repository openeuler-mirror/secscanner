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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0206_accountToHome():
    InsertSection("check if account has its own home directory")
    if os.path.exists('/etc/passwd'):
        ret, users = subprocess.getstatusoutput("grep -E -v '^(halt|sync|shutdown)' /etc/passwd")
        count1 = 0
        count2 = 0
        if ret == 0:
            users = [line.split(':') for line in users.strip().split('\n') if line.split(':')[6] not in ['/bin/false', '/sbin/nologin', '/usr/sbin/nologin']]
            for user in users:
                name = user[0]
                home = user[5]
                if not os.path.isdir(home):
                    count1 += 1
                else:
                    ret, result = subprocess.getstatusoutput(f'ls -l -d {home}')
                    if ret == 0:
                        owner = result.split()[2]

                    if owner != name:
                        count2 += 1

            if count1 == 0 and count2 == 0:
                logger.info("Confirm that the account has its own home directory, checking ok")
                Display("- check if account has its own home directory...", "OK")
            elif count1 > 0 and count2 == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0206\n")
                logger.warning("WRN_C0206_01: %s", WRN_C0206_01)
                logger.warning("SUG_C0206_01: %s", SUG_C0206_01)
                Display("- At least one account does not have a home folder ...", "WARNING")
            elif count2 > 0 and count1 == 0:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0206\n")
                logger.warning("WRN_C0206_02: %s", WRN_C0206_02)
                logger.warning("SUG_C0206_01: %s", SUG_C0206_01)
                Display("- At least one home directory does not match the user ...", "WARNING")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0206\n")
                logger.warning("WRN_C0206_03: %s", WRN_C0206_03)
                logger.warning("SUG_C0206_01: %s", SUG_C0206_01)
                Display("- There are issues with the user and their home directory ...", "WARNING")

        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0206\n")
            logger.warning("WRN_C0206_04: %s", WRN_C0206_04)
            logger.warning("SUG_C0206_01: %s", SUG_C0206_01)
            Display("- Failed to obtain passwd user list ...", "FAILED")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0206\n")
        logger.warning("WRN_C0206_05: %s", WRN_C0206_05)
        logger.warning("SUG_C0206_02: %s", SUG_C0206_02)
        Display("- file /etc/passwd not exists...", "SKIPPING")