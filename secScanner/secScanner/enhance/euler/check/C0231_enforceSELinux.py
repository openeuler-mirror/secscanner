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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

# grep -Ei '^\s*SELINUX=(enforcing|permissive)'/etc/selinux/config
def C0231_enforceSELinux():
    InsertSection("check the selinux set")
    config_file = "/etc/selinux/config"
    if os.path.exists(config_file):
        IS_EXIST = 0
        with open("/etc/selinux/config", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'^\s*SELINUX=(enforcing|permissive)', line):
                    IS_EXIST = 1

        if IS_EXIST == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0231\n")
            logger.warning("WRN_C0231: %s", WRN_C0231)
            logger.warning("SUG_C0231: %s", SUG_C0231)
            Display("- Wrong selinux set...", "WARNING")
        else:
            logger.info("Has right selinux set, checking ok")
            Display("- Has right selinux set ...", "OK")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0231\n")
        logger.warning(f"WRN_C0231: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0231: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
