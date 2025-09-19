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

logger = logging.getLogger("secscanner")


def S0201_lockUnUsedUser():
    InsertSection("Lock the unused users...")
    set_disable_unused_user = seconf.get('euler', 'disable_unused_user')
    unused_user_value = seconf.get('euler', 'unused_user_value').split()

    if set_disable_unused_user == 'yes':
        for i in unused_user_value:
            ret, result = subprocess.getstatusoutput(f'usermod -L -s /bin/false {i}')
            if ret != 0:
                logger.warning(f'{result}')

        logger.info("lock the unused user successfully")
        Display("- lock the unused user ...", "FINISHED")
    else:
        Display("- Skip lock the unused users, due to config file...", "SKIPPING")
