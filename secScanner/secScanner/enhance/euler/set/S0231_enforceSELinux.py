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

import subprocess
import os
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
logger = logging.getLogger("secscanner")


def S0231_enforceSELinux():
    InsertSection("Enforce the selinux...")
    # check system archtecture
    ret, sys_arch = subprocess.getstatusoutput('uname -m')
    if sys_arch not in ['aarch64', 'x86_64']:
        Display("- Skip set selinux for sw/loongarch...", "SKIPPING")
        return
    SET_SELINUX = seconf.get('euler', 'set_selinux')
    if SET_SELINUX == 'yes':
        if os.path.exists('/etc/selinux/config'):
            if not os.path.exists('/etc/selinux/config_bak') and os.path.exists('/etc/selinux/config'):
                shutil.copy2('/etc/selinux/config', '/etc/selinux/config_bak')
            add_bak_file('/etc/selinux/config_bak')
            SET_STATUS = 0
            with open('/etc/selinux/config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^\s*SELINUX=(enforcing|permissive)', line):
                        SET_STATUS = 1
                        # Display("- Has right set of selinux ...", "SKIPPING")
                    elif re.search(r'^\s*SELINUX=disabled', line):
                        SET_STATUS = -1
                    else:
                        continue

            if SET_STATUS == 1:
                Display("- Has right set of selinux ...", "SKIPPING")
            elif SET_STATUS == -1:
                with open('/etc/selinux/config', 'w') as write_file:
                    for line in lines:
                        if re.search(r'^\s*SELINUX=disabled', line):
                            write_file.write('SELINUX=permissive\n')
                        else:
                            write_file.write(line)
            else:
                with open('/etc/selinux/config', 'a') as add_file:
                    add_file.write('\nSELINUX=permissive\n')
            #check again
            RIGHT_SET = 0
            with open('/etc/selinux/config', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^\s*SELINUX=(enforcing|permissive)', line):
                        RIGHT_SET = 1
            if RIGHT_SET == 1:
                logger.info("Set selinux, checking ok")
                Display("- Set selinux...", "FINISHED")
            else:
                logger.info("Set selinux failed")
                Display("- Set selinux failed...", "FAILED")
        else:
            logger.warning("selinux config file not exist")
            Display("- selinux config file not exist", "FAILED")

    else:
        Display("- Skip set selinux due to config file...", "SKIPPING")
