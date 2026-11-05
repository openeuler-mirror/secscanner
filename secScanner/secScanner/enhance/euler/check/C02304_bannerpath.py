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
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C02304_bannerpath():
    '''
    Function: check that the banner path is configured correctly
    '''
    InsertSection("check that the banner path is configured correctly")
    config_file = "/etc/ssh/sshd_config"
    if os.path.exists(config_file):
        banner_path = ''
        with open(config_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match(r'\s*Banner\s+', line, re.IGNORECASE):
                    fields = line.strip().split()
                    if len(fields) > 1:
                        banner_path = fields[1]
        if banner_path == '':
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02304\n")
            logger.warning("WRN_C02304_01: %s", WRN_C02304_01)
            logger.warning("SUG_C02304_01: %s", SUG_C02304_01)
            Display("- No Banner set in /etc/ssh/sshd_config...", "WARNING")
        elif not os.path.exists(banner_path):
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02304\n")
            logger.warning("WRN_C02304_02: %s", WRN_C02304_02)
            logger.warning("SUG_C02304_02: %s", SUG_C02304_02)
            Display(f"- Banner file {banner_path} does not exist...", "WARNING")
        else:
            logger.info("Banner path is configured correctly, checking ok")
            Display(f"- Has Banner set to {banner_path} in /etc/ssh/sshd_config...", "OK")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02304\n")
        logger.warning(f"WRN_C02304: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C02304: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")

