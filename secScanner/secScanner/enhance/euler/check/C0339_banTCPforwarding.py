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
def C0339_banTCPforwarding():
    InsertSection("Check set of AllowTcpForwarding in sshd config file")
    config_file = "/etc/ssh/sshd_config"
    if os.path.exists(config_file):
        flag1 = False
        flag2 = False
        cmd1 = "grep -Ei '^\s*AllowTcpForwarding\s+no' /etc/ssh/sshd_config"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        if ret1 == 0 and result1 == "AllowTcpForwarding no":
            flag1 = True
        cmd2 = "grep -Ei '^\s*AllowTcpForwarding\s+yes' /etc/ssh/sshd_config"
        ret2, result2 = subprocess.getstatusoutput(cmd2)
        if ret2 == 1 and result2 == "":
            flag2 = True

        if flag1 and flag2:
            logger.info("Check set of AllowTcpForwarding in sshd config file")
            Display("- Check set of AllowTcpForwarding in sshd config file", "OK")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0339\n")
            logger.warning("WRN_C0339: %s", WRN_C0339)
            logger.warning("SUG_C0339: %s", SUG_C0339)
            Display("- Wrong set of AllowTcpForwarding in sshd config file...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0339\n")
        logger.warning(f"WRN_C0339: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0339: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
