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

def C0243_enANDdePolicy():
    InsertSection("check global encryption and decryption policies set...")
    if os.path.exists('/etc/crypto-policies/config'):
        CHECK_EXIST = 0
        with open('/etc/crypto-policies/config', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('DEFAULT', line):
                    CHECK_EXIST = 1

        if CHECK_EXIST == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0243\n")
            logger.warning("WRN_C0243_01: %s", WRN_C0243_01)
            logger.warning("SUG_C0243_01: %s", SUG_C0243_01)
            Display("- No global encryption and decryption policy set ...", "WARNING")
        else:
            logger.info("Confirm that global encryption and decryption policies have been set")
            Display("- check global encryption and decryption policies set...", "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0243\n")
        logger.warning("WRN_C0243_02: %s", WRN_C0243_02)
        logger.warning("SUG_C0243_02: %s", SUG_C0243_02)
        Display("- file /etc/crypto-policies/config does not exist...", "WARNING")
