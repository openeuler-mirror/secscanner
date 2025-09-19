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


import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S0243_enANDdePolicy():
    set_encryption_decryption_policy = seconf.get('euler', 'set_encryption_decryption_policy')
    InsertSection("Set global encryption and decryption policies...")
    if set_encryption_decryption_policy == 'yes':
        if os.path.exists('/etc/crypto-policies/config'):
            if not os.path.exists('/etc/crypto-policies/config_bak'):
                shutil.copy2('/etc/crypto-policies/config', '/etc/crypto-policies/config_bak')
            add_bak_file('/etc/crypto-policies/config_bak')

            IS_EXIST = 0
            with open('/etc/crypto-policies/config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('DEFAULT', line):
                        IS_EXIST = 1
            if IS_EXIST == 0:
                with open('/etc/crypto-policies/config', 'a') as add_file:
                    add_file.write("\nDEFAULT\n")
            else:
                with open('/etc/crypto-policies/config', 'w') as write_file:
                    for line in lines:
                        write_file.write(line)

            CHECK_EXIST = 0
            with open('/etc/crypto-policies/config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('DEFAULT', line):
                        CHECK_EXIST = 1
            if CHECK_EXIST == 0:
                logger.warning("NO encryption and decryption policies set, setting failed")
                Display("- NO encryption and decryption policies set...", "FAILED")
            else:
                logger.info("Has encryption and decryption policies set, seting ok")
                Display("- Set encryption and decryption policies...", "FINISHED")

        else:
            logger.warning("file /etc/crypto-policies/config does not exist, setting failed")
            Display("- file /etc/crypto-policies/config does not exist...", "FAILED")

    else:
        Display(f"- Skip set encryption and decryption policies due to config file...", "SKIPPING")
