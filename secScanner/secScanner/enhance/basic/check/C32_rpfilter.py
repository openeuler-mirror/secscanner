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


def C32_rpfilter():
    InsertSection("check the reverse path filtering")
    all_set = 'unset'
    default_set = 'unset'
    with open("/etc/sysctl.conf", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('net.ipv4.conf.all.rp_filter', line) and not re.match('^#|^$', line):
                all_set = 'wrong'
                temp = line.split('=')
                if len(temp) == 2 and temp[1] == '1\n':
                    all_set = 'right'
            if re.match('net.ipv4.conf.default.rp_filter', line) and not re.match('^#|^$', line):
                default_set = 'wrong'
                temp = line.split('=')
                if len(temp) == 2 and temp[1] == '1\n':
                    default_set = 'right'
    if all_set == 'unset' and default_set == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC32\n")
        logger.warning("WRN_C32_01: %s", WRN_C32_01)
        logger.warning("SUG_C32: %s", SUG_C32)
        Display("- No reverse path filtering config set...", "WARNING")
    elif all_set == 'right' and default_set == 'right':
        logger.info("Has reverse path filtering set, checking OK")
        Display("- Check the reverse path filtering set...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC32\n")
        logger.warning("WRN_C32_02: %s", WRN_C32_02)
        logger.warning("SUG_C32: %s", SUG_C32)
        Display("- Wrong reverse path filtering config set...", "WARNING")
