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

content_to_write = """
polkit.addAdminRule(function(action, subject) {
    return ["unix-user:0"];
});
"""

def C0236_setPkexec():
    InsertSection("check ordinary users cannot use pkexec to configure root privileges set")
    file_path = '/etc/polkit-1/rules.d/50-default.rules'
    if os.path.exists(file_path):
        exist = False
        with open(file_path, 'r') as file:
            existing_content = file.read()
            if content_to_write not in existing_content:
                exist = False
            else:
                exist = True

        if exist:
            logger.info("check ordinary users cannot use pkexec to configure root privileges, checking ok")
            Display("- check ordinary users cannot use pkexec to configure root privileges set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0236\n")
            logger.warning("WRN_C0236_01: %s", WRN_C0236_01)
            logger.warning("SUG_C0236_01: %s", SUG_C0236_01)
            Display("- NO ordinary users cannot use pkexec to configure root privileges set...", "WARNING")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0236\n")
        logger.warning("WRN_C0236_02: %s", WRN_C0236_02)
        logger.warning("SUG_C0236_02: %s", SUG_C0236_02)
        Display("- file /etc/polkit-1/rules.d/50-default.rules does not exist...", "WARNING")
