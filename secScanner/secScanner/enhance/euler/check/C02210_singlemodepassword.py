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

def C02210_singlemodepassword():
    '''
    Function: check that single user mode is protected with a password
    '''
    InsertSection("check that single user mode is protected with a password")
    service_files = ['/usr/lib/systemd/system/rescue.service', '/usr/lib/systemd/system/emergency.service']
    wrns = [WRN_C02210_01, WRN_C02210_02]
    sugs = [SUG_C02210_01, SUG_C02210_02]
    texts = ['- No systemd-sulogin-shell set in /usr/lib/systemd/system/rescue.service...',
             '- No systemd-sulogin-shell set in /usr/lib/systemd/system/emergency.service...']
    ok_texts = ['- Has systemd-sulogin-shell set in /usr/lib/systemd/system/rescue.service...',
                '- Has systemd-sulogin-shell set in /usr/lib/systemd/system/emergency.service...']

    for index, service_file in enumerate(service_files):
        wrn_name = f"WRN_C02210_{index+1:02d}"
        sug_name = f"SUG_C02210_{index+1:02d}"
        if os.path.exists(service_file):
            item_ok = False
            with open(service_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.match(r'\s*ExecStart', line) and '/systemd-sulogin-shell' in line:
                        item_ok = True
            if item_ok:
                logger.info(f"single user mode password protection is set in {service_file}, checking ok")
                Display(ok_texts[index], "OK")
            else:
                with open(RESULT_FILE, "a", encoding="utf-8") as file:
                    file.write("\nC02210\n")
                logger.warning(f"{wrn_name}: %s", wrns[index])
                logger.warning(f"{sug_name}: %s", sugs[index])
                Display(texts[index], "WARNING")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02210\n")
            logger.warning(f"{wrn_name}: {service_file} {WRN_no_file}")
            logger.warning(f"{sug_name}: {service_file} {SUG_no_file}")
            Display(f"- Config file: {service_file} not found...", "SKIPPING")

