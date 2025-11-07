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

def C122_sshLoginTMOUT():
    InsertSection("check the SSH login timeout...")
    ClientAliveInterval_set = 'unset'
    ClientAliveCountMax_set = 'unset'
    if os.path.exists('/etc/ssh/sshd_config'):
        with open('/etc/ssh/sshd_config', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('ClientAliveInterval', line) and not re.match('^#|^$', line):
                    ClientAliveInterval_set = 'set'
                    temp = line.split()
                    if len(temp) == 2 and temp[1].isdigit() and 0 < int(temp[1]) <= 900:
                        ClientAliveInterval_set = 'right'

                if re.match('ClientAliveCountMax', line) and not re.match('^#|^$', line):
                    ClientAliveCountMax_set = 'set'
                    temp = line.split()
                    if len(temp) == 2 and temp[1] == '0':
                        ClientAliveCountMax_set = 'right'


        if ClientAliveInterval_set == 'right' and ClientAliveCountMax_set == 'right':
            logger.info("Has ssh login timeout set, checking OK")
            Display("- Has ssh login timeout set...", "OK")
        elif ClientAliveInterval_set == 'set' and ClientAliveCountMax_set == 'set':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC122\n")
            logger.warning("WRN_C122_01: %s", WRN_C122_01)
            logger.warning("SUG_C122_01: %s", SUG_C122_01)
            Display("- Wrong ssh login timeout set...", "WARNING")
        elif ClientAliveInterval_set == 'unset' and ClientAliveCountMax_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC122\n")
            logger.warning("WRN_C122_02: %s", WRN_C122_02)
            logger.warning("SUG_C122_01: %s", SUG_C122_01)
            Display("- No ssh login timeout set...", "WARNING")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC122\n")
            logger.warning("WRN_C122_03: %s", WRN_C122_03)
            logger.warning("SUG_C122_01: %s", SUG_C122_01)
            Display("- SSH login connection timeout configuration issue...", "WARNING")
    else:
        logger.warning("WRN_C122_04: %s", WRN_C122_04)
        logger.warning("SUG_C122_02: %s", SUG_C122_02)
        Display("- file /etc/ssh/sshd_config does not exist...", "WARNING")

