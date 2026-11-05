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

def C02205_stronghash():
    '''
    Function: check that the password is encrypted with strong hash algorithm
    '''
    InsertSection("check that the password is encrypted with strong hash algorithm")
    checks = []

    # item 1: pam_unix sha512 in /etc/pam.d/system-auth
    item1_ok = False
    item1_missing = not os.path.exists('/etc/pam.d/system-auth')
    if not item1_missing:
        with open('/etc/pam.d/system-auth', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line) and re.search('sha512', line):
                    item1_ok = True
    checks.append([item1_ok, item1_missing])

    # item 2: ENCRYPT_METHOD SHA512 in /etc/login.defs
    item2_ok = False
    item2_missing = not os.path.exists('/etc/login.defs')
    if not item2_missing:
        with open('/etc/login.defs', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match(r'\s*ENCRYPT_METHOD\s+', line) and re.search('SHA512', line):
                    item2_ok = True
    checks.append([item2_ok, item2_missing])

    # item 3: crypt_style sha512 in /etc/libuser.conf
    item3_ok = False
    item3_missing = not os.path.exists('/etc/libuser.conf')
    if not item3_missing:
        with open('/etc/libuser.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.match(r'\s*crypt_style\s*=', line) and re.search('sha512', line, re.IGNORECASE):
                    item3_ok = True
    checks.append([item3_ok, item3_missing])

    wrns = [WRN_C02205_01, WRN_C02205_02, WRN_C02205_03]
    sugs = [SUG_C02205_01, SUG_C02205_02, SUG_C02205_03]
    texts = ['- No sha512 set for pam_unix in /etc/pam.d/system-auth...',
             '- No ENCRYPT_METHOD SHA512 set in /etc/login.defs...',
             '- No crypt_style sha512 set in /etc/libuser.conf...']
    ok_texts = ['- Has sha512 set for pam_unix in /etc/pam.d/system-auth...',
                '- Has ENCRYPT_METHOD SHA512 set in /etc/login.defs...',
                '- Has crypt_style sha512 set in /etc/libuser.conf...']
    config_files = ['/etc/pam.d/system-auth', '/etc/login.defs', '/etc/libuser.conf']

    for index, (item_ok, item_missing) in enumerate(checks):
        wrn_name = f"WRN_C02205_{index+1:02d}"
        sug_name = f"SUG_C02205_{index+1:02d}"
        if item_missing:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02205\n")
            logger.warning(f"{wrn_name}: {config_files[index]} {WRN_no_file}")
            logger.warning(f"{sug_name}: {config_files[index]} {SUG_no_file}")
            Display(f"- Config file: {config_files[index]} not found...", "SKIPPING")
        elif not item_ok:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02205\n")
            logger.warning(f"{wrn_name}: %s", wrns[index])
            logger.warning(f"{sug_name}: %s", sugs[index])
            Display(texts[index], "WARNING")
        else:
            logger.info(f"strong hash algorithm is set in {config_files[index]}, checking ok")
            Display(ok_texts[index], "OK")

