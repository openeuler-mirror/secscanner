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


def S38_limitUserResources():
    set_limit_resources= seconf.get('basic', 'set_limit_resources')
    InsertSection("Set the limit of system resources...")
    if set_limit_resources == 'yes':
        if os.path.exists('/etc/security/limits.conf') and not os.path.exists('/etc/security/limits.conf_bak'):
            shutil.copy2('/etc/security/limits.conf', '/etc/security/limits.conf_bak')
        add_bak_file('/etc/security/limits.conf_bak')
        if os.path.exists('/etc/pam.d/login') and not os.path.exists('/etc/pam.d/login_bak'):
            shutil.copy2('/etc/pam.d/login', '/etc/pam.d/login_bak')
        add_bak_file('/etc/pam.d/login_bak')
        if os.path.exists('/etc/security/limits.conf'):
            set01 = False
            set02 = False
            set03 = False
            set04 = False
            set05 = False
            set_pam = False
            with open('/etc/security/limits.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('soft', line) and re.search('stack', line):
                        set01 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('stack', line):
                        set02 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('rss', line):
                        set03 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('nproc', line):
                        set04 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('maxlogin', line):
                        set05 = True

            if not (set01 and set02 and set03 and set04 and set05):
                with open('/etc/security/limits.conf', 'a') as add_file:
                    add_file.write("\n* soft stack 1024\n* hard stack 1024\n* hard rss 100000\n* hard nproc 4000\n* hard maxlogins 3")
            else:
                pass
           
            with open('/etc/pam.d/login', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('session', line) and re.search('/lib64/security/pam_limits.so', line):
                        set_pam = True
            
            if not set_pam:
                with open('/etc/pam.d/login', 'a') as add_file:
                    add_file.write("session    required     /lib64/security/pam_limits.so\n")
            else:
                pass

            with open('/etc/security/limits.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('soft', line) and re.search('stack', line):
                        set01 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('stack', line):
                        set02 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('rss', line):
                        set03 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('nproc', line):
                        set04 = True
                    if (not re.match('#|$', line)) and re.search('hard', line) and re.search('maxlogin', line):
                        set05 = True
           
            with open('/etc/pam.d/login', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.match('session', line) and re.search('/lib64/security/pam_limits.so', line):
                        set_pam = True

            if set01 and set02 and set03 and set04 and set05 and set_pam: 
                logger.info("set the limit of system resources successfully")
                Display(f"- Setting the the limit of system resources...", "FINISHED")

            else:
                logger.info("Set the limit of system resources failed")
                Display("- Set the the limit of system resources...", "FAILED")

        else:
            logger.info("no filepath /etc/security/limits.conf")
            Display("- no filepath /etc/security/limits.conf...", "SKIPPING")
    else:
        Display(f"- Skip set the limit of system resources...", "SKIPPING")
