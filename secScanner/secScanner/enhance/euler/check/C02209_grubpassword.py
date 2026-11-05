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

def C02209_grubpassword():
    '''
    Function: check that grub is protected with a password
    '''
    InsertSection("check that grub is protected with a password")
    grub_dirs = []
    if os.path.isdir('/boot/efi/EFI/openEuler'):
        grub_dirs.append('/boot/efi/EFI/openEuler')
    if os.path.isdir('/boot/grub2'):
        grub_dirs.append('/boot/grub2')
    if not grub_dirs:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC02209\n")
        logger.warning("WRN_C02209: /boot/efi/EFI/openEuler or /boot/grub2 %s", WRN_no_file)
        logger.warning("SUG_C02209: /boot/efi/EFI/openEuler or /boot/grub2 %s", SUG_no_file)
        Display("- Grub config directory not found...", "SKIPPING")
    else:
        cfg_ok = False
        user_ok = False
        for grub_dir in grub_dirs:
            grub_cfg = os.path.join(grub_dir, 'grub.cfg')
            user_cfg = os.path.join(grub_dir, 'user.cfg')
            if os.path.exists(grub_cfg):
                with open(grub_cfg, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        if 'password_pbkdf2' in line or 'grub.pbkdf2.sha512' in line:
                            cfg_ok = True
            if os.path.exists(user_cfg):
                with open(user_cfg, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        if re.search(r'GRUB2_PASSWORD=grub\.pbkdf2\.sha512\.\d+\.', line):
                            user_ok = True
        if cfg_ok and user_ok:
            logger.info("grub password protection is set, checking ok")
            Display("- Has grub password protection set...", "OK")
        if not cfg_ok:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02209\n")
            logger.warning("WRN_C02209_01: %s", WRN_C02209_01)
            logger.warning("SUG_C02209_01: %s", SUG_C02209_01)
            Display("- No password_pbkdf2 set in grub.cfg...", "WARNING")
        if not user_ok:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC02209\n")
            logger.warning("WRN_C02209_02: %s", WRN_C02209_02)
            logger.warning("SUG_C02209_02: %s", SUG_C02209_02)
            Display("- No GRUB2_PASSWORD set in user.cfg...", "WARNING")

