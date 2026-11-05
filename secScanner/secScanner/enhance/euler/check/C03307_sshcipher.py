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

def C03307_sshcipher():
    """Check the SSH ciphers algorithms in sshd config file."""
    InsertSection("Check set of Ciphers in sshd config file")
    config_file = "/etc/ssh/sshd_config"
    safe_ciphers = ["aes128-ctr", "aes192-ctr", "aes256-ctr", "chacha20-poly1305@openssh.com", "aes128-gcm@openssh.com", "aes256-gcm@openssh.com"]
    if os.path.exists(config_file):
        flag = False
        with open(config_file, "r") as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match("Ciphers", line, re.IGNORECASE):
                    temp = line.split()
                    if len(temp) >= 2:
                        algos = temp[1].split(",")
                        if all(algo in safe_ciphers for algo in algos):
                            flag = True
        if flag:
            logger.info("Check set of Ciphers in sshd config file")
            Display("- Check set of Ciphers in sshd config file", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC03307\n")
            logger.warning("WRN_C03307: %s", WRN_C03307)
            logger.warning("SUG_C03307: %s", SUG_C03307)
            Display("- Wrong set of Ciphers in sshd config file...", "WARNING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03307\n")
        logger.warning(f"WRN_C03307: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C03307: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
