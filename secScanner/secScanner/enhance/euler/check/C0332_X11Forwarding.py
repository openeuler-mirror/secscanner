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
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")
def C0332_X11Forwarding():
    InsertSection("Check set of X11forwarding in sshd config file")
    config_file = "/etc/ssh/sshd_config"
    if os.path.exists(config_file):
        flag = False
        with open("/etc/ssh/sshd_config", "r") as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match("X11Forwarding", line):
                    if re.search("no", line):
                        flag = True
                        break
        if flag:
            logger.info("Check set of X11forwarding in sshd config file")
            Display("- Check set of X11forwarding in sshd config file", "OK")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0332\n")
            logger.warning("WRN_C0332: %s", WRN_C0332)
            logger.warning("SUG_C0332: %s", SUG_C0332)
            Display("- Wrong set of X11forwarding in sshd config file...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0332\n")
        logger.warning(f"WRN_C0332: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0332: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
