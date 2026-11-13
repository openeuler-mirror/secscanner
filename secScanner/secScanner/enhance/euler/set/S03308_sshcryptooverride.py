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
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S03308_sshcryptooverride():
    """Remove the crypto policy override of sshd service."""
    InsertSection("Set config of sshd crypto policy override...")
    set_flag = seconf.get('euler', 'set_sshcryptooverride')
    if set_flag == 'yes':
        if os.path.exists('/etc/sysconfig/sshd'):
            if not os.path.exists('/etc/sysconfig/sshd_bak'):
                shutil.copy2('/etc/sysconfig/sshd', '/etc/sysconfig/sshd_bak')
            add_bak_file('/etc/sysconfig/sshd_bak')
            exist = False
            with open("/etc/sysconfig/sshd", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r"\s*CRYPTO_POLICY=", line):
                        value = line.split("=", 1)[1].strip().strip("'\"")
                        if value:
                            exist = True
            if not exist:
                logger.info("Check crypto policy override of sshd right")
                Display("- Already no crypto policy override in /etc/sysconfig/sshd", "FINISHED")
                return
            with open("/etc/sysconfig/sshd", "w") as write_file:
                for line in lines:
                    if re.match(r"\s*CRYPTO_POLICY=", line) and line.split("=", 1)[1].strip().strip("'\""):
                        write_file.write("# " + line)
                    else:
                        write_file.write(line)
            flag = True
            with open("/etc/sysconfig/sshd", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r"\s*CRYPTO_POLICY=", line):
                        value = line.split("=", 1)[1].strip().strip("'\"")
                        if value:
                            flag = False
                            break
            if flag:
                logger.info("Remove crypto policy override of sshd finish")
                Display("- Comment crypto policy override in /etc/sysconfig/sshd and reload sshd service", "FINISHED")
            else:
                logger.warning("Remove crypto policy override of sshd failed")
                Display("- Remove crypto policy override in /etc/sysconfig/sshd", "FAILED")
        else:
            logger.info("file /etc/sysconfig/sshd does not exist, no crypto policy override")
            Display("- Already no crypto policy override in /etc/sysconfig/sshd", "FINISHED")
    else:
        Display("Skip set sshd crypto policy override due to config file...", "SKIPPING")
