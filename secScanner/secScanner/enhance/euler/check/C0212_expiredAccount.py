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
import datetime
logger = logging.getLogger("secscanner")

def C0212_expiredAccount():
    InsertSection("check for expired account")
    if os.path.exists('/etc/shadow'):
        expired_accounts = False
        current_date = int(datetime.datetime.now().timestamp())

        with open('/etc/shadow', 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                username = parts[0]
                expire_date = parts[7]

                if expire_date:
                    expire_date_seconds = int(expire_date) * 86400

                    if expire_date_seconds < current_date:
                        expired_accounts = True

        if expired_accounts:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0212\n")
            logger.warning("WRN_C0212_01: %s", WRN_C0212_01)
            logger.warning("SUG_C0212_01: %s", SUG_C0212_01)
            Display("- At least one account has expired", "WARNING")
        else:
            logger.info('No expired account exists, checking ok')
            Display("- No expired account exists", "OK")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0212\n")
        logger.warning("WRN_C0212_02: %s", WRN_C0212_02)
        logger.warning("SUG_C0212_02: %s", SUG_C0212_02)
        Display("- file /etc/shadow dose not exist...", "WARNING")