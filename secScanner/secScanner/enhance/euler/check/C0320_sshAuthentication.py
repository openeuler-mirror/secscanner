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
此处IgnoreRhosts必须配置为yes，
HostbasedAuthentication必须配置为no，
PasswordAuthentication、ChallengeResponseAuthentication和PubkeyAuthentication至少有一个为yes
'''
def C0320_sshAuthentication():
    InsertSection("Check config of ssh authentication")
    config_file = "/etc/ssh/sshd_config"
    if os.path.exists(config_file):
        ignore_rhosts_flag = False
        HostbasedAuthentication_flag = False
        other_flag = False
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('IgnoreRhosts', line):
                    if 'yes' in line:
                        ignore_rhosts_flag = True
                if re.match('HostbasedAuthentication', line):
                    if 'no' in line:
                        HostbasedAuthentication_flag = True
                if re.match('PasswordAuthentication', line) or re.match('ChallengeResponseAuthentication', line) or re.match('PubkeyAuthentication', line):
                    if 'yes' in line:
                        other_flag = True
        if ignore_rhosts_flag and HostbasedAuthentication_flag and other_flag:
            logger.info("Check config of ssh authentication")
            Display("- Check config of ssh authentication", "OK")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0320\n")
            logger.warning("WRN_C0320: %s", WRN_C0320)
            logger.warning("SUG_C0320: %s", SUG_C0320)
            Display("- Check wrong set of ssh authentication...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0320\n")
        logger.warning(f"WRN_C0320: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0320: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
