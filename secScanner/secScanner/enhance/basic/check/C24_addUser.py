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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def C24_addUser():
    InsertSection("check whether have the customer user")
    count_user = 0
    ADV_OPTIONS = seconf.options('advance')#search basic and show all options
    USER_NAME = ''
    if ('username' in ADV_OPTIONS):# if there is a 'userName', save the value
        USER_NAME = seconf.get('advance', 'username')

    with open('/etc/passwd', 'r') as file:
        lines = file.readlines()
        for line in lines:
            temp = line.split(':', -1)
            if temp[0] == USER_NAME:
                count_user = count_user + 1
    if USER_NAME == '':
        logger.info("No vaild userName found, please check config file...")
        Display("- No vaild userName found, please check config file...",  "FAILED")
    else:
        if count_user == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC24\n")
            logger.warning("WRN_C24: %s", WRN_C24)
            logger.warning("SUG_C24: %s", SUG_C24)
            Display("- No additional user found, check warning", "WARNING")
        else:
            logger.info(f"Already have {USER_NAME}, no need to add")
            Display(f"- Already have {USER_NAME}...", "OK")


