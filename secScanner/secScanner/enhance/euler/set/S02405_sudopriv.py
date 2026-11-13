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
import shutil
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02405_sudopriv():
    '''
    Function: ensure that normal users can run privileged programs through sudo
    '''
    InsertSection("set normal users to run privileged programs through sudo...")
    set_flag = seconf.get('euler', 'set_sudopriv')
    if set_flag == 'yes':
        ret, res = subprocess.getstatusoutput('rpm -q sudo')
        if ret != 0:
            logger.warning("sudo is not installed, please install it manually")
            Display("- sudo is not installed, please install it manually...", "FAILED")
        elif not os.path.exists('/etc/sudoers'):
            logger.warning("file /etc/sudoers does not exist")
            Display("- File /etc/sudoers does not exist...", "FAILED")
        else:
            root_rule = False
            wheel_rule = False
            commented_wheel = False
            with open('/etc/sudoers', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match(r'\s*#', line):
                        if re.search(r'\(root\)|\(ALL', line):
                            root_rule = True
                        if re.match(r'\s*%wheel\s+ALL=', line) and re.search(r'\(root\)|\(ALL', line):
                            wheel_rule = True
                    if re.match(r'\s*#\s*%wheel\s+ALL=', line):
                        commented_wheel = True
            if root_rule and wheel_rule:
                logger.info("sudo rule is already set for normal users")
                Display("- Already set normal users to run privileged programs through sudo...", "SKIPPING")
            else:
                if not os.path.exists('/etc/sudoers_bak'):
                    shutil.copy2('/etc/sudoers', '/etc/sudoers_bak')
                add_bak_file('/etc/sudoers_bak')
                new_lines = []
                wheel_added = False
                for line in lines:
                    if (not wheel_rule) and commented_wheel and re.match(r'\s*#\s*%wheel\s+ALL=', line):
                        new_line = re.sub(r'^(\s*)#\s*%', r'\1%', line)
                        new_lines.append(new_line)
                        wheel_added = True
                    else:
                        new_lines.append(line)
                if (not wheel_rule) and not commented_wheel:
                    new_lines.append('%wheel\tALL=(ALL)\tALL\n')
                    wheel_added = True
                with open('/etc/sudoers', 'w') as write_file:
                    write_file.writelines(new_lines)
                ret2, res2 = subprocess.getstatusoutput('visudo -c')
                if ret2 != 0:
                    logger.warning(f"visudo check failed: {res2}")
                    shutil.copy2('/etc/sudoers_bak', '/etc/sudoers')
                    Display("- Set normal users to run privileged programs through sudo...", "FAILED")
                else:
                    check_root_rule = False
                    check_wheel_rule = False
                    with open('/etc/sudoers', 'r') as read_file:
                        check_lines = read_file.readlines()
                        for line in check_lines:
                            if not re.match(r'\s*#', line):
                                if re.search(r'\(root\)|\(ALL', line):
                                    check_root_rule = True
                                if re.match(r'\s*%wheel\s+ALL=', line) and re.search(r'\(root\)|\(ALL', line):
                                    check_wheel_rule = True
                    if check_root_rule and check_wheel_rule:
                        logger.info("set normal users to run privileged programs through sudo successfully")
                        Display("- Set normal users to run privileged programs through sudo...", "FINISHED")
                    else:
                        logger.warning("set normal users to run privileged programs through sudo failed")
                        Display("- Set normal users to run privileged programs through sudo...", "FAILED")
    else:
        Display("- Skip set normal users to run privileged programs through sudo...", "SKIPPING")

