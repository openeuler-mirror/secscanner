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

def C423_dhcpDisabled():
    InsertSection("check if dhcp service is disabled")
    cmd_audit = "systemctl is-enabled dhcpd"
    ret, result = subprocess.getstatusoutput(cmd_audit)
    if ret == 1 and result in ['disabled', 'masked']:
        logger.info("Has right dhcp service set, checking ok")
        Display(f"- Has right dhcp service set: {result}...", "OK")
    elif ret == 1 and 'Failed to get unit file state' in result:
        logger.info("No dhcp service, checking ok")
        Display("- No dhcp service, checking ok...", "OK")
    elif ret == 0 and result == "enabled":
        with open(RESULT_FILE, "a") as file:
            file.write("\nC423\n")
        logger.warning("WRN_C423: %s", WRN_C423)
        logger.warning("SUG_C423: %s", SUG_C423)
        Display("- Wrong dhcp service status...", "WARNING")
    else:
        logger.info("Unexpected status of dhcpd")
        Display("- Unexpected status of dhcpd...", "WARNING")