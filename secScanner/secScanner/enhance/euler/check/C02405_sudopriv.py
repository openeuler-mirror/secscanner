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
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C02405_sudopriv():
    '''
    Function: check that normal users can run privileged programs through sudo
    '''
    InsertSection("check that normal users can run privileged programs through sudo")
    ret, res = subprocess.getstatusoutput('rpm -q sudo')
    if ret == 0:
        logger.info("sudo is installed, checking ok")
        Display("- Has sudo installed...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02405\n")
        logger.warning("WRN_C02405_01: %s", WRN_C02405_01)
        logger.warning("SUG_C02405_01: %s", SUG_C02405_01)
        Display("- sudo is not installed...", "WARNING")

    if os.path.exists('/etc/sudoers'):
        root_rule = False
        wheel_rule = False
        with open('/etc/sudoers', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if not re.match(r'\s*#', line):
                    if re.search(r'\(root\)|\(ALL', line):
                        root_rule = True
                    if re.match(r'\s*%wheel\s+ALL=', line) and re.search(r'\(root\)|\(ALL', line):
                        wheel_rule = True
        if root_rule:
            logger.info("(root) sudo rule is configured in /etc/sudoers, checking ok")
            Display("- Has (root) sudo rule set in /etc/sudoers...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02405\n")
            logger.warning("WRN_C02405_02: %s", WRN_C02405_02)
            logger.warning("SUG_C02405_02: %s", SUG_C02405_02)
            Display("- No (root) sudo rule set in /etc/sudoers...", "WARNING")
        if wheel_rule:
            logger.info("wheel group sudo rule is enabled in /etc/sudoers, checking ok")
            Display("- Has wheel group sudo rule set in /etc/sudoers...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02405\n")
            logger.warning("WRN_C02405_03: %s", WRN_C02405_03)
            logger.warning("SUG_C02405_03: %s", SUG_C02405_03)
            Display("- No wheel group sudo rule set in /etc/sudoers...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02405\n")
        logger.warning("WRN_C02405: /etc/sudoers %s", WRN_no_file)
        logger.warning("SUG_C02405: /etc/sudoers %s", SUG_no_file)
        Display("- Config file: /etc/sudoers not found...", "SKIPPING")

