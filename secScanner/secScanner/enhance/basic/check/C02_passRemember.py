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


def C02_passRemember():
    InsertSection("check passwd Remember times")
    SET_VAL1 = []
    SET_VAL2 = []
    with open("/etc/pam.d/password-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                    and re.search('enforce_for_root', line) and re.search('remember=', line):
                regex = r'(?<=remember=).[0-9]*'
                SET_VAL1 = re.findall(regex, line)
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                    and re.search('enforce_for_root', line) and re.search('remember=', line):
                regex = r'(?<=remember=).[0-9]*'
                SET_VAL2 = re.findall(regex, line)
    if SET_VAL1 == [] or SET_VAL2 == []:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC02\n")
        logger.warning("WRN_C02_01: %s", WRN_C02_01)
        logger.warning("SUG_C02: %s", SUG_C02)
        Display("- No Password Remember set...", "WARNING")
    elif int(SET_VAL1[0]) > 4 and int(SET_VAL2[0]) > 4:
        logger.info("has passwd Remember times set, checking ok")
        Display("- Has Password Remember set...", "OK")
    elif (int(SET_VAL1[0]) <= 4 and int(SET_VAL1[0]) > 0) or (int(SET_VAL2[0]) <= 4 and int(SET_VAL2[0]) > 0):
        logger.warning("WRN_C02_02: %s", WRN_C02_02)
        logger.warning("SUG_C02: %s", SUG_C02)
        Display("- Password Remember times is not right...", "WARNING")
    else:
        Display("- Password Remember times is invalid...", "WARNING")
