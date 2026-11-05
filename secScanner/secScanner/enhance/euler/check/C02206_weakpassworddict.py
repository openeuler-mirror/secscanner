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

def C02206_weakpassworddict():
    '''
    Function: check that the weak password dictionary is set correctly
    '''
    InsertSection("check that the weak password dictionary is set correctly")
    checks = []

    # item 1: pam_pwquality enabled in /etc/pam.d/system-auth
    item1_ok = False
    item1_missing = not os.path.exists('/etc/pam.d/system-auth')
    if not item1_missing:
        with open('/etc/pam.d/system-auth', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwquality.so', line):
                    item1_ok = True
    checks.append([item1_ok, item1_missing])

    # item 2: no dictcheck=0 for pam_pwquality in /etc/pam.d/system-auth
    item2_ok = True
    item2_missing = False
    if not item1_missing:
        with open('/etc/pam.d/system-auth', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('dictcheck=0', line):
                    item2_ok = False
    checks.append([item2_ok, item2_missing])

    # item 3: no dictcheck=0 in /etc/security/pwquality.conf
    item3_ok = True
    item3_missing = not os.path.exists('/etc/security/pwquality.conf')
    if not item3_missing:
        with open('/etc/security/pwquality.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match(r'\s*dictcheck\s*=\s*0', line):
                    item3_ok = False
    checks.append([item3_ok, item3_missing])

    # item 4: cracklib dictionary exists
    item4_ok = os.path.exists('/usr/share/cracklib/pw_dict.hwm')
    checks.append([item4_ok, False])

    wrns = [WRN_C02206_01, WRN_C02206_02, WRN_C02206_03, WRN_C02206_04]
    sugs = [SUG_C02206_01, SUG_C02206_02, SUG_C02206_03, SUG_C02206_04]
    texts = ['- No pam_pwquality set in /etc/pam.d/system-auth...',
             '- dictcheck=0 set for pam_pwquality in /etc/pam.d/system-auth...',
             '- dictcheck=0 set in /etc/security/pwquality.conf...',
             '- No cracklib weak password dictionary in /usr/share/cracklib...']
    ok_texts = ['- Has pam_pwquality set in /etc/pam.d/system-auth...',
                '- No dictcheck=0 set for pam_pwquality in /etc/pam.d/system-auth...',
                '- No dictcheck=0 set in /etc/security/pwquality.conf...',
                '- Has cracklib weak password dictionary in /usr/share/cracklib...']
    config_files = ['/etc/pam.d/system-auth', '/etc/pam.d/system-auth',
                    '/etc/security/pwquality.conf', '/usr/share/cracklib']

    for index, (item_ok, item_missing) in enumerate(checks):
        wrn_name = f"WRN_C02206_{index+1:02d}"
        sug_name = f"SUG_C02206_{index+1:02d}"
        if item_missing:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02206\n")
            logger.warning(f"{wrn_name}: {config_files[index]} {WRN_no_file}")
            logger.warning(f"{sug_name}: {config_files[index]} {SUG_no_file}")
            Display(f"- Config file: {config_files[index]} not found...", "SKIPPING")
        elif not item_ok:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02206\n")
            logger.warning(f"{wrn_name}: %s", wrns[index])
            logger.warning(f"{sug_name}: %s", sugs[index])
            Display(texts[index], "WARNING")
        else:
            logger.info(f"weak password dictionary check {config_files[index]} is ok")
            Display(ok_texts[index], "OK")

