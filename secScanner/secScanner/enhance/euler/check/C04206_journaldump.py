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

def C04206_journaldump():
    '''
    Function: Check whether the rsyslog dumps journald logs in /etc/rsyslog.conf
    '''
    InsertSection("Check the rsyslog dump journald log config in /etc/rsyslog.conf")
    config_file = "/etc/rsyslog.conf"
    if not os.path.exists(config_file):
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04206\n")
        logger.warning("WRN_C04206: %s %s", config_file, WRN_no_file)
        logger.warning("SUG_C04206: %s %s", config_file, SUG_no_file)
        Display(f"- {config_file} does not exist...", "SKIPPING")
        return
    IS_EXIST = 0
    with open(config_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            if (not re.match('#|$', line)) and re.search('imjournal', line):
                IS_EXIST = 1

    if IS_EXIST == 0:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04206\n")
        logger.warning("WRN_C04206: %s", WRN_C04206)
        logger.warning("SUG_C04206: %s", SUG_C04206)
        Display("- The rsyslog dump journald log is not configured in /etc/rsyslog.conf...", "WARNING")
    else:
        logger.info("The rsyslog dump journald log is configured, checking OK")
        Display("- Check the rsyslog dump journald log config...", "OK")
