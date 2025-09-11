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
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *

logger = logging.getLogger("secscanner")


def C0201_lockUnUsedUser():
    InsertSection("check the unused user")
    unuser_user = seconf.get('euler', 'unused_user_value').split()
    error_user = []
    counter = 0

    for i in unuser_user:
        try:
            output = subprocess.check_output(["grep", "-i", f"^{i}:", "/etc/shadow"])
            output = output.decode("utf-8").strip()
            if "!*" not in output:
                error_user.append(i)
                counter += 1
        except subprocess.CalledProcessError:
            pass

    if counter > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0201\n")
        logger.warning(f"WRN_C0201: These users: {error_user} should lock")
        logger.warning("SUG_C0201: %s", SUG_C0201)
        Display("- Check if there have unused user...", "WARNING")
    else:
        logger.info("All unused user is locked, checking ok")
        Display("- Check if there have unused user...", "OK")
