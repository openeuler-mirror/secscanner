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


def S18_syslogKern():
    SET_RECORDING_KERNEL_WARN= seconf.get('basic', 'recording_kernel_warn')
    KERNEL_WARN_FILE_NAME = seconf.get('basic', 'kernel_warn_file_name')
    InsertSection("Recording the kernel warn...")
    if SET_RECORDING_KERNEL_WARN == 'yes':
        if os.path.exists('/etc/rsyslog.conf') and not os.path.exists('/etc/rsyslog.conf_bak'):
            shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
        add_bak_file('/etc/rsyslog.conf_bak')
        if os.path.exists('/etc/rsyslog.conf'):
            IS_EXIST = 0
            with open('/etc/rsyslog.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('kern.warning', line) and re.search('/var/log', line):
                        IS_EXIST = 1

            if IS_EXIST == 0:
                with open('/etc/rsyslog.conf', 'a') as add_file:
                    add_file.write(f"\nkern.warning /var/log/{KERNEL_WARN_FILE_NAME}\n")
            else:
                logger.info("has kern.warn set, passing...")
            Display(f"- Setting the rsyslog.conf, recording the kern warn...", "FINISHED")

        else:
            logger.info("no filepath /etc/rsyslog.conf")
            Display("- no filepath /etc/rsyslog.conf...", "SKIPPING")

    else:
        Display(f"- Skip recording the kernel warn due to config file...", "SKIPPING")
