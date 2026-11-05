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

def C03306_sshmacs():
    """Check the SSH message authentication codes algorithms in sshd config file."""
    InsertSection("Check set of MACs in sshd config file")
    config_file = "/etc/ssh/sshd_config"
    safe_macs = ["hmac-sha2-512", "hmac-sha2-512-etm@openssh.com", "hmac-sha2-256", "hmac-sha2-256-etm@openssh.com"]
    if os.path.exists(config_file):
        flag = False
        with open(config_file, "r") as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match("MACs", line, re.IGNORECASE):
                    temp = line.split()
                    if len(temp) >= 2:
                        algos = temp[1].split(",")
                        if all(algo in safe_macs for algo in algos):
                            flag = True
        if flag:
            logger.info("Check set of MACs in sshd config file")
            Display("- Check set of MACs in sshd config file", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03306\n")
            logger.warning("WRN_C03306: %s", WRN_C03306)
            logger.warning("SUG_C03306: %s", SUG_C03306)
            Display("- Wrong set of MACs in sshd config file...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03306\n")
        logger.warning(f"WRN_C03306: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C03306: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
