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


def C12_sshGssapi():
    InsertSection("check the ssh gssapi")
    GSSAPI_VAL = ''
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('^GSSAPIAuthentication', line) and (not re.match('^#|^$', line)):
                temp = line.split()
                if len(temp) == 2:  # check if there is only one word after GSSAPIAuthentication
                    GSSAPI_VAL = temp[1]  # umask 022 UMASK_VAL: 022
    if GSSAPI_VAL == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC12\n")
        logger.warning("WRN_C12_02: %s", WRN_C12_02)
        logger.warning("SUG_C12: %s", SUG_C12)
        Display("- No ssh gssapi config set...", "WARNING")
    elif GSSAPI_VAL.lower() == 'no':
        logger.warning("Has ssh gssapi set, checking ok")
        Display("- Check the ssh gssapi...", "OK")
    else:
        logger.warning("WRN_C12_01: %s", WRN_C12_01)
        logger.warning("SUG_C12: %s", SUG_C12)
        Display("- Wrong ssh gssapi config set...", "WARNING")

