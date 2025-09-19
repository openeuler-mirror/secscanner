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

def S0204_rootUIDunique():
    InsertSection("Make the root UID unique")
    rootUID_unique = seconf.get('euler', 'rootUID_unique')
    if rootUID_unique == 'yes':
        if os.path.exists('/etc/passwd'):
            if not os.path.exists('/etc/passwd_bak'):
                shutil.copy2('/etc/passwd', '/etc/passwd_bak')
            add_bak_file('/etc/passwd_bak')

            with open('/etc/passwd', 'r') as file:
                lines = file.readlines()

            filtered_lines = []

            for line in lines:
                if line.split(':')[2] != '0' or line.split(':')[0] == 'root':
                    filtered_lines.append(line)

            with open('/etc/passwd', 'w') as file:
                file.writelines(filtered_lines)

            command = "awk -F: '($3 == 0) { print $1 }' /etc/passwd"
            ret, result = subprocess.getstatusoutput(command)
            if ret == 0:
                if not result.strip():
                    logger.info("No UID 0 users (except root) found in /etc/passwd")
                    Display("- No UID 0 users (except root) found ...", "FINISHED")
                else:
                    result = result.strip().split('\n')
                    if len(result) == 1 and result[0] == 'root':
                        logger.info("root is the only UID 0 user")
                        Display("- root is the only UID 0 user ...", "FINISHED")
            else:
                logger.warning("Failed to obtain information with UID 0")
                Display("- Failed to obtain information with UID 0 ...", "FAILED")
        else:
            logger.warning("file /etc/passwd does not exist")
            Display("- file /etc/passwd not exists...", "SKIPPING")

    else:
        Display("- Skip confirm if the root UID is unique due to config file...", "SKIPPING")

