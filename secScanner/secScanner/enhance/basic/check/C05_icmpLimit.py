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


def C05_icmpLimit():
    InsertSection("check icmp redirect limit")
    ICMP_EXIST = 0
    with open("/etc/sysctl.conf", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('net.ipv4.conf.all.accept_redirects=0', line) and (not re.match('#|$', line)):
                ICMP_EXIST = 1

    if ICMP_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC05\n")
        logger.warning("WRN_C05: %s", WRN_C05)
        logger.warning("SUG_C05: %s", SUG_C05)
        Display("- Wrong icmp limit set...", "WARNING")
    else:
        logger.info("Has icmp redirect limit set, checking ok")
        Display("- Has icmp redirect limit set...", "OK")
