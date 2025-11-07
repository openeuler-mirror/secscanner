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

def C0238_denyRootLocalaccess():
    InsertSection("check prevent root users from accessing the system locally")
    if os.path.exists('/etc/pam.d/system-auth'):
        pam_access_module = "pam_access.so"
        pam_access_found = False
        with open('/etc/pam.d/system-auth', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if pam_access_module in line:
                    pam_access_found = True

        deny_tty1 = '-:root:tty1'
        tty1_exist = False
        with open('/etc/security/access.conf', 'r') as f:
            acclines = f.readlines()
            for line in acclines:
                if (not re.match('#|$', line)) and deny_tty1 in line:
                    tty1_exist = True

        if pam_access_found and tty1_exist:
            logger.info("check prevent root users from accessing the system locally, checking ok")
            Display("- check prevent root users from accessing the system locally...", "OK")

        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0238\n")
            logger.warning("WRN_C0238_01: %s", WRN_C0238_01)
            logger.warning("SUG_C0238_01: %s", SUG_C0238_01)
            Display("- NO prevent root users from accessing the system locally set...", "WARNING")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0238\n")
        logger.warning("WRN_C0238_02: %s", WRN_C0238_02)
        logger.warning("SUG_C0238_02: %s", SUG_C0238_02)
        Display("- file /etc/pam.d/system-auth does not exist...", "WARNING")



