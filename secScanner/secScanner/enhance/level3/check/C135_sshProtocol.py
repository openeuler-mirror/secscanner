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


def C135_sshProtocol():
    InsertSection("check the ssh Protocol set...")
    if os.path.exists('/etc/ssh/sshd_config'):

        check_exist = False
        with open('/etc/ssh/sshd_config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('Protocol', line) and re.search('2', line):
                    temp = line.strip('\n').split()
                    if temp[0] == 'Protocol' and temp[1] == '2':
                        check_exist = True

        if not check_exist:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC135\n")
            logger.warning("WRN_C135_01: %s", WRN_C135_01)
            logger.warning("SUG_C135_01: %s", SUG_C135_01)
            Display("- Set the ssh Protocol...", "WARNING")
        else:
            logger.info("ssh Protocol set exists, checking ok")
            Display("- check the ssh Protocol...", "OK")

    else:   
        with open(RESULT_FILE, "a") as file:
            file.write("\nC135\n")
        logger.warning("WRN_C135_02: %s", WRN_C135_02)
        logger.warning("SUG_C135_02: %s", SUG_C135_02)
        Display("- file /etc/ssh/sshd_config does not exist...", "WARNING")
