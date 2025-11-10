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


import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import subprocess
logger = logging.getLogger("secscanner")

def S05_icmpLimit():
    InsertSection("Disable the icmp redirect...")
    disable_icmp_redirect = seconf.get('basic', 'disable_icmp_redirect')
    if disable_icmp_redirect == 'yes':
        if os.path.exists('/etc/sysctl.conf') and not os.path.exists('/etc/sysctl.conf_bak'):
            shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        add_bak_file('/etc/sysctl.conf_bak')
        if os.path.exists('/etc/sysctl.conf'):
            ACCEPT_REDIRECT_SET = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('accept_redirects', line):
                        ACCEPT_REDIRECT_SET = 1
            if ACCEPT_REDIRECT_SET == 0:
                with open('/etc/sysctl.conf', 'a') as add_file:
                    add_file.write('\nnet.ipv4.conf.all.accept_redirects=0\n')
            else:
                with open('/etc/sysctl.conf', 'w') as write_file:
                    for line in lines:
                        if not re.match('#|$', line) and re.search('accept_redirects', line):
                            write_file.write('net.ipv4.conf.all.accept_redirects=0\n')
                        else:
                            write_file.write(line)
            ret, result = subprocess.getstatusoutput('sysctl -p -q')
            if ret != 0:
                logger.warning('Command execution failed')

            IS_EXIST = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('accept_redirects', line):
                        IS_EXIST = 1
            if IS_EXIST == 1:
                logger.info("Set the icmp redirect, checking ok")
                Display("- Set the icmp redirect...", "FINISHED")
            else:
                logger.info("Set the icmp redirect failed")
                Display("- Set the icmp redirect...", "FAILED")
        else:
            logger.info("Set the icmp redirect failed")
            Display("- No filepath /etc/sysctl.conf...", "FAILED")
    else:
        Display("- Skip disable the icmp redirect due to config file...", "SKIPPING")
