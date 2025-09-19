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

def S0206_accountToHome():
    InsertSection("Confirm that the account has its own home directory")
    account_to_home = seconf.get('euler','account_to_home')
    if account_to_home == 'yes':
        if os.path.exists('/etc/passwd'):
            if not os.path.exists('/etc/passwd_bak'):
                shutil.copy2('/etc/passwd', '/etc/passwd_bak')
            add_bak_file('/etc/passwd_bak')
            if not os.path.exists('/etc/shadow_bak'):
                shutil.copy2('/etc/shadow', '/etc/shadow_bak')
            add_bak_file('/etc/shadow_bak')

            count1 = 0
            count2 = 0
            ret, users = subprocess.getstatusoutput("grep -E -v '^(halt|sync|shutdown)' /etc/passwd")
            if ret == 0:
                users = [line.split(':') for line in users.strip().split('\n') if line.split(':')[6] not in ['/bin/false', '/sbin/nologin', '/usr/sbin/nologin']]
                for user in users:
                    name = user[0]
                    home = user[5]
                    if not os.path.isdir(home):
                        ret, delresult = subprocess.getstatusoutput(f'userdel -r {name}')
                        if ret == 0:
                            flag, out = subprocess.getstatusoutput(f'useradd {name}')
                    else:
                        ret, result = subprocess.getstatusoutput(f'ls -l -d {home}')
                        if ret == 0:
                            owner = result.split()[2]
                             
                        if owner != name:
                            ret, delresult = subprocess.getstatusoutput(f'userdel -r {name}')
                            if ret == 0:
                                flag, out = subprocess.getstatusoutput(f'useradd {name}')

            ret, users = subprocess.getstatusoutput("grep -E -v '^(halt|sync|shutdown)' /etc/passwd")
            if ret == 0:
                users = [line.split(':') for line in users.strip().split('\n') if line.split(':')[6] not in ['/bin/false', '/sbin/nologin', '/usr/sbin/nologin']]
                for user in users:
                    name = user[0]
                    home = user[5]
                    if not os.path.isdir(home):
                        count1 += 1
                    else:
                        ret, result = subprocess.getstatusoutput(f'ls -l -d {home}')
                        if ret == 0:
                            owner = result.split()[2]
                        if owner != name:
                            count2 += 1
                
                if count1 == 0 and count2 == 0:
                    logger.info("Confirm that the account has its own home directory")
                    Display("- Confirm that the account has its own home directory...", "FINISHED")
                elif count1 > 0 and count2 == 0:
                    logger.warning("At least one account does not have a home folder")
                    Display("- At least one account does not have a home folder...", "FAILED")
                elif count1 == 0  and count2 > 0:
                    logger.warning("At least one home directory does not match the user")
                    Display("- At least one home directory does not match the user", "FAILED")
                else:
                    logger.warning("There are issues with the user and their home directory")
                    Display("- There are issues with the user and their home directory", "FAILED")
            
                            
            else:
                logger.warning("Failed to obtain passwd user list")
                Display("- Failed to obtain passwd user list ...", "FAILED")

        else:
            logger.warning("file /etc/passwd does not exist")
            Display("- file /etc/passwd not exists...", "SKIPPING")

    else:
        Display("- Skip confirm if the account has its own home directory due to config file...", "SKIPPING")

