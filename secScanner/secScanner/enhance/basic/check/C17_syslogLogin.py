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


def C17_syslogLogin():
    InsertSection("check if record the user login events")
    SYSLOG_CONF = ['/etc/rsyslog.conf']
    count = 0
    for i in SYSLOG_CONF:
        if os.path.isfile(i) and os.path.getsize(i) > 0:
            #check file exist and not empty
            with open(i, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('authpriv.info', line) and re.search('/var/log/', line) and not re.match('#', line):
                        count = count + 1
            if count == 0:
                with open(RESULT_FILE, "a", encoding="utf-8") as file:
                    file.write("\nC17\n")
                logger.warning("WRN_C17: %s", WRN_C17)
                logger.warning("SUG_C17: %s", SUG_C17)
                Display("- Check if there have authpriv.info set...", "WARNING")
            else:
                logger.info("The security audit modle authpriv.info is set, checking OK")
                Display("- Check if there have authpriv.info set...", "OK")
        else:
            Display(f"- file {i} does not exist...", "SKIPPED")
