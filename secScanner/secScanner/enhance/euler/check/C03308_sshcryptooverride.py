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

def C03308_sshcryptooverride():
    """Check the crypto policy override of sshd service."""
    InsertSection("Check crypto policy override of sshd")
    config_file = "/etc/sysconfig/sshd"
    if os.path.exists(config_file):
        flag = False
        with open(config_file, "r") as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match(r"\s*CRYPTO_POLICY=", line):
                    value = line.split("=", 1)[1].strip().strip("'\"")
                    if value:
                        flag = True
        if flag:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03308\n")
            logger.warning("WRN_C03308: %s", WRN_C03308)
            logger.warning("SUG_C03308: %s", SUG_C03308)
            Display("- Found crypto policy override of sshd...", "WARNING")
        else:
            logger.info("Check crypto policy override of sshd")
            Display("- Check crypto policy override of sshd", "OK")
    else:
        logger.info("file /etc/sysconfig/sshd does not exist, no crypto policy override")
        Display("- Check crypto policy override of sshd", "OK")
