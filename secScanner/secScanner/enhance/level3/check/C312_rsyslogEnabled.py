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

#audit_result=$(systemctl is-enabled rsyslog)
def C312_rsyslogEnabled():
    InsertSection("check the rsyslog service is enabled")
    service_name = "rsyslog"
    cmd_rsyslog = "systemctl is-enabled rsyslog"
    ret, result = subprocess.getstatusoutput(cmd_rsyslog)
    if ret == 1 and result in ['disabled', 'masked']:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC312\n")
        logger.warning("WRN_C312: %s", WRN_C312_01)
        logger.warning("SUG_C312: %s", SUG_C312_01)
        Display(f"- Wrong {service_name} service status...", "WARNING")
    elif ret == 1 and 'Failed to get unit file state' in result:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC312\n")
        logger.warning("WRN_C312: %s", WRN_C312_02)
        logger.warning("SUG_C312: %s", SUG_C312_02)
        Display(f"- No {service_name} service, need to install...", "WARNING")
    elif ret == 0 and result == "enabled":
        logger.info(f"Has right {service_name} service set, checking ok")
        Display(f"- Has right {service_name} service set: {result}...", "OK")
    else:
        logger.info(f"Unexpected status of {service_name}")
        Display(f"- Unexpected status of {service_name}...", "WARNING")