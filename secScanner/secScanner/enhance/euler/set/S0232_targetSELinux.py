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

def S0232_targetSELinux(): 
    InsertSection("set SELinux policy...")
    # check system archtecture
    ret, sys_arch = subprocess.getstatusoutput('uname -m')
    if sys_arch not in ['aarch64', 'x86_64']:
        Display("- Skip set selinux for sw/loongarch...", "SKIPPING")
        return
    set_selinux_policy = seconf.get('euler', 'set_selinux_policy')
    if set_selinux_policy == 'yes':
        ret, result = subprocess.getstatusoutput("sestatus | grep 'Loaded policy name'")
        if ret == 0:
            result = result.split(':')[1].strip()
            if result == 'targeted':
                logger.info("SELinux policy configuration is correct")
                Display("- SELinux policy configuration is correct...", "FINISHED")
                return
            else:
                if os.path.exists('/etc/selinux/config'):
                    if not os.path.exists('/etc/selinux/config_bak'):
                        shutil.copy2('/etc/selinux/config', '/etc/selinux/config_bak')
                    add_bak_file('/etc/selinux/config_bak')

                    out, output = subprocess.getstatusoutput("rpm -q selinux-policy-targeted")
                    if out == 0 and output != '':
                        pass
                    else:
                        out, output = subprocess.getstatusoutput("yum install selinux-policy-targeted -y")
                        if out == 0 and output != '':
                            pass
                        else:
                            logger.warning("Failed to install targeted policy package")
                            Display("- Failed to install targeted policy package...", "FAILED")
                            return
                    set_status = 0
                    with open('/etc/selinux/config', 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.search('SELINUXTYPE', line) and not re.match('#|$', line):
                                set_status = -1
                                temp = line.strip('\n').split('=')
                                if temp[0] == 'SELINUXTYPE' and temp[1] == 'targeted':
                                    set_status = 1

                    if set_status == 1:
                        logger.info("Already has right set of SELinux target")
                        Display("- Already has right set of SELinux target ...", "FINISHED")
                        return
                    elif set_status == -1:
                        with open('/etc/selinux/config', 'w') as write_file:
                            for line in lines:
                                if re.match('SELINUXTYPE', line):
                                    write_file.write("SELINUXTYPE=targeted")
                                    pathlib.Path('/.autorelabel').touch()
                                else:
                                    write_file.write(line)
                                    pathlib.Path('/.autorelabel').touch()
                    else:
                        with open('/etc/selinux/config', 'a') as add_file:
                            add_file.write("\nSELINUXTYPE=targeted\n")
                            pathlib.Path('/.autorelabel').touch()

                    check_status = 0
                    with open('/etc/selinux/config', 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.search('SELINUXTYPE', line) and not re.match('#|$', line):
                                check_status = -1
                                temp = line.strip('\n').split('=')
                                if temp[0] == 'SELINUXTYPE' and temp[1] == 'targeted':
                                    check_status = 1
                    if check_status == 1:
                        logger.info("SELinux policy set successfully")
                        Display("- SELinux policy set successfully...", "FINISHED")
                    elif check_status == -1:
                        logger.warning("Incorrect SELinux policy settings")
                        Display("- Incorrect SELinux policy settings...", "FAILED")
                    else:
                        logger.warning("No SELinux policy settings")
                        Display("- No SELinux policy settings...", "FAILED")
                else:
                    logger.warning("file /etc/selinux/config does not exist")
                    Display("- file /etc/selinux/config does not exist...", "FAILED")

        else:
            logger.warning("Failed to obtain SELinux policy")
            Display("- Failed to obtain SELinux policy...", "FAILED")
    else:
        Display("- Skip set SELinux policy due to config file...", "SKIPPING")

