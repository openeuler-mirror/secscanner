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

def C02204_pwordaccount():
    '''
    Function: check that the password does not contain the account string
    '''
    InsertSection("check that the password does not contain the account string")
    config_files = ['/etc/pam.d/system-auth', '/etc/pam.d/password-auth']
    wrns = [WRN_C02204_01, WRN_C02204_02, WRN_C02204_03, WRN_C02204_04]
    sugs = [SUG_C02204_01, SUG_C02204_02, SUG_C02204_03, SUG_C02204_04]
    texts = ['- No pam_pwquality set in /etc/pam.d/system-auth...',
             '- usercheck=0 set in /etc/pam.d/system-auth...',
             '- No pam_pwquality set in /etc/pam.d/password-auth...',
             '- usercheck=0 set in /etc/pam.d/password-auth...']
    checks = []
    for index, config_file in enumerate(config_files):
        enabled = False
        usercheck_zero = False
        file_missing = not os.path.exists(config_file)
        if not file_missing:
            with open(config_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_pwquality.so', line):
                        enabled = True
                        if re.search('usercheck=0', line):
                            usercheck_zero = True
        checks.append([enabled, usercheck_zero, file_missing])

    for index, (enabled, usercheck_zero, file_missing) in enumerate(checks):
        offset = index * 2
        if file_missing:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02204\n")
            logger.warning(f"WRN_C02204_{offset+1:02d}: {config_files[index]} {WRN_no_file}")
            logger.warning(f"SUG_C02204_{offset+1:02d}: {config_files[index]} {SUG_no_file}")
            Display(f"- Config file: {config_files[index]} not found...", "SKIPPING")
        elif not enabled:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02204\n")
            logger.warning(f"WRN_C02204_{offset+1:02d}: %s", wrns[offset])
            logger.warning(f"SUG_C02204_{offset+1:02d}: %s", sugs[offset])
            Display(texts[offset], "WARNING")
        elif usercheck_zero:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02204\n")
            logger.warning(f"WRN_C02204_{offset+2:02d}: %s", wrns[offset+1])
            logger.warning(f"SUG_C02204_{offset+2:02d}: %s", sugs[offset+1])
            Display(texts[offset+1], "WARNING")
        else:
            logger.info(f"pam_pwquality is enabled and no usercheck=0 set in {config_files[index]}, checking ok")
            Display(f"- Has pam_pwquality set without usercheck=0 in {config_files[index]}...", "OK")

