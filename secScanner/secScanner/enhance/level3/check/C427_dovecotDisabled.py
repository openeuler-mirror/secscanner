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

def C427_dovecotDisabled():
    InsertSection("check if IMAP and POP3 service is disabled")
    service_name = "dovecot"
    cmd_audit = "systemctl is-enabled dovecot"
    ret, result = subprocess.getstatusoutput(cmd_audit)
    if ret == 1 and result in ['disabled', 'masked']:
        logger.info(f"Has right {service_name} service set, checking ok")
        Display(f"- Has right {service_name} service set: {result}...", "OK")
    elif ret == 1 and 'Failed to get unit file state' in result:
        logger.info(f"No {service_name} service, checking ok")
        Display(f"- No {service_name} service, checking ok...", "OK")
    elif ret == 0 and result == "enabled":
        with open(RESULT_FILE, "a") as file:
            file.write("\nC427\n")
        logger.warning("WRN_C427: %s", WRN_C427)
        logger.warning("SUG_C427: %s", SUG_C427)
        Display(f"- Wrong {service_name} service status...", "WARNING")
    else:
        logger.info(f"Unexpected status of {service_name}")
        Display(f"- Unexpected status of {service_name}...", "WARNING")