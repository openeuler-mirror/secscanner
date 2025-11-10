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
'''
# grep "^PubkeyAcceptedKeyTypes" /etc/ssh/sshd_config
PubkeyAcceptedKeyTypes ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-512
'''
def C0322_pubkeyTypes():
    InsertSection("Check set of PubkeyAcceptedKeyTypes")
    config_file = "/etc/ssh/sshd_config"
    if os.path.exists(config_file):
        types = ["ssh-ed25519", "ssh-ed25519-cert-v01@openssh.com", "rsa-sha2-256", "rsa-sha2-512"]
        pubkey_flag = False
        flag = True
        with open("/etc/ssh/sshd_config", "r") as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match("PubkeyAcceptedKeyTypes", line):
                    pubkey_flag = True
                    for single_type in types:
                        if single_type not in line:
                            flag = False
        if pubkey_flag:
            if flag:
                logger.info("Check set of PubkeyAcceptedKeyTypes")
                Display("- Check set of PubkeyAcceptedKeyTypes", "OK")
            else:
                with open(RESULT_FILE, 'a') as file:
                    file.write("\nC0322\n")
                logger.warning("WRN_C0322: %s", WRN_C0322_01)
                logger.warning("SUG_C0322: %s", SUG_C0322_01)
                Display("- Wrong set of PubkeyAcceptedKeyTypes...", "WARNING")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0322\n")
            logger.warning("WRN_C0322: %s", WRN_C0322_02)
            logger.warning("SUG_C0322: %s", SUG_C0322_02)
            Display("- Wrong set of PubkeyAcceptedKeyTypes...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0322\n")
        logger.warning(f"WRN_C0322: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0322: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
