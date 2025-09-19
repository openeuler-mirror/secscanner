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
import logging
import shutil
import datetime
logger = logging.getLogger("secscanner")


def S0212_expiredAccount():
    InsertSection("Delete expired account")
    expired_account = seconf.get('euler', 'expired_account')
    if expired_account == 'yes':
        if os.path.exists('/etc/shadow'):
            if not os.path.exists('/etc/shadow_bak'):
                shutil.copy2('/etc/shadow', '/etc/shadow_bak')
            add_bak_file('/etc/shadow_bak')

            expired_accounts = False
            current_date = int(datetime.datetime.now().timestamp())

            # Open the /etc/shadow file and read the lines
            with open('/etc/shadow', 'r') as file:
                for line in file:
                    # Split the line by ':'
                    parts = line.strip().split(':')

                    # Get the username and expiration date
                    username = parts[0]
                    expire_date = parts[7]

                    # Check if the expiration date is set
                    if expire_date:
                        # Convert the expiration date to seconds since the epoch
                        expire_date_seconds = int(expire_date) * 86400

                        # Check if the expiration date is before the current date
                        if expire_date_seconds < current_date:
                            expired_accounts = True
                            ret, result = subprocess.getstatusoutput(f'userdel -r {username}')
                            if ret == 0:
                                expired_accounts = False

            if expired_accounts:
                logger.warning('At least one account has expired.')
                Display("- At least one account has expired", "FAILED")
            else:
                logger.info('No expired account exists')
                Display("- No expired account exists", "FINISHED")

        else:
            logger.warning("file /etc/shadow dose not exist")
            Display("- file /etc/shadow dose not exist...", "SKIPPING")

    else:
        Display("- Skip check for expired account due to config file...", "SKIPPING")
