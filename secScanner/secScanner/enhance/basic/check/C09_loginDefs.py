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


def C09_loginDefs():
    InsertSection("check the password lifetime in /etc/login.defs")
    PASS_MAX_DAYS_VAL = ''  # if not match PASS_MAX_DAYS, PASS_MAX_DAYS_VAL = ''
    PASS_MIN_DAYS_VAL = ''
    PASS_MIN_LEN_VAL = ''
    PASS_WARN_AGE_VAL = ''

    # search part
    with open("/etc/login.defs", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('PASS_MAX_DAYS', line) and (not re.match('#', line)):
                temp = line.split()  # if no number after PASS_MAX_DAYS, len(temp) == 1
                if len(temp) == 2 and temp[1].isdigit():  # check if there is only one number after PASS_MAX_DAYS
                    PASS_MAX_DAYS_VAL = temp[1]  # PASS_MAX_DAYS 90 ---> PASS_MAX_DAYS_VAL == '90'

            if re.match('PASS_MIN_DAYS', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2 and temp[1].isdigit():
                    PASS_MIN_DAYS_VAL = temp[1]
            if re.match('PASS_MIN_LEN', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2 and temp[1].isdigit():
                    PASS_MIN_LEN_VAL = temp[1]
            if re.match('PASS_WARN_AGE', line) and (not re.match('#', line)):
                temp = line.split()
                if len(temp) == 2 and temp[1].isdigit():
                    PASS_WARN_AGE_VAL = temp[1]

    # decide part
    # ------------------------------------------------------------------------------------------------
    if PASS_MAX_DAYS_VAL == '':
        # PASS_MAX_DAYS not found or no numbers after PASS_MAX_DAYS_VAL
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_02: %s", WRN_C09_02)
        logger.warning("SUG_C09_01: %s", SUG_C09_01)
        Display("- PASS_MAX_DAYS value is null...", "WARNING")
    elif int(PASS_MAX_DAYS_VAL) > 90:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_01: %s", WRN_C09_01)
        logger.warning("SUG_C09_01: %s", SUG_C09_01)
        Display("- PASS_MAX_DAYS value is not safe...", "WARNING")
    else:
        logger.info("PASS_MAX_DAYS value is safe, checking OK")
        Display("- Check the PASS_MAX_DAYS value...", "OK")

    # ------------------------------------------------------------------------------------------------
    if PASS_MIN_DAYS_VAL == '':
        # PASS_MAX_DAYS not found or no numbers after PASS_MAX_DAYS_VAL
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_03: %s", WRN_C09_03)
        logger.warning("SUG_C09_02: %s", SUG_C09_02)
        Display("- PASS_MIN_DAYS value is null...", "WARNING")
    elif int(PASS_MIN_DAYS_VAL) < 6:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_04: %s", WRN_C09_04)
        logger.warning("SUG_C09_02: %s", SUG_C09_02)
        Display("- PASS_MIN_DAYS value is not safe...", "WARNING")
    else:
        logger.info("PASS_MIN_DAYS value is safe, checking OK")
        Display("- Check the PASS_MIN_DAYS value...", "OK")

    # ------------------------------------------------------------------------------------------------
    if PASS_MIN_LEN_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.info("WRN_C09_06: %s", WRN_C09_06)
        logger.warning("SUG_C09_03: %s", SUG_C09_03)
        Display("- PASS_MIN_LEN value is null...", "WARNING")
    elif int(PASS_MIN_LEN_VAL) < 10:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_05: %s", WRN_C09_05)
        logger.warning("SUG_C09_03: %s", SUG_C09_03)
        Display("- PASS_MIN_LEN value is not safe...", "WARNING")
    else:
        logger.info("PASS_MIN_LEN value is safe, checking OK")
        Display("- Check the PASS_MIN_LEN value...", "OK")

    # ------------------------------------------------------------------------------------------------
    if PASS_WARN_AGE_VAL == '':
        # PASS_MAX_DAYS not found or no numbers after PASS_MAX_DAYS_VAL
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_08: %s", WRN_C09_08)
        logger.warning("SUG_C09_04: %s", SUG_C09_04)
        Display("- PASS_WARN_AGE value is null...", "WARNING")
    elif int(PASS_WARN_AGE_VAL) < 30:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC09\n")
        logger.warning("WRN_C09_07: %s", WRN_C09_07)
        logger.warning("SUG_C09_04: %s", SUG_C09_04)
        Display("- PASS_WARN_AGE value is not safe...", "WARNING")
    else:
        logger.info("PASS_WARN_AGE value is safe, checking OK")
        Display("- Check the PASS_WARN_AGE value...", "OK")
