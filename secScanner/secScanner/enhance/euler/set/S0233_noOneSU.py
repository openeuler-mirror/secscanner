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


def S0233_noOneSU():
    SET_FORBIDDEN_SU = seconf.get('euler', 'forbidden_to_su')
    InsertSection("No one can su to root")
    if SET_FORBIDDEN_SU == 'yes':
        if os.path.exists('/etc/pam.d/su') and not os.path.exists('/etc/pam.d/su_bak'):
            shutil.copy2('/etc/pam.d/su', '/etc/pam.d/su_bak')
        add_bak_file('/etc/pam.d/su_bak')

        IS_EXIST = 0
        GROUP_EXIST = 0
        with open('/etc/pam.d/su', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('auth', line) and re.search('pam_wheel.so', line) \
                        and re.search('use_uid', line):
                    IS_EXIST = 1
                    if re.search('group=wheel', line):
                        GROUP_EXIST = 1

        if IS_EXIST == 0:
            logger.info("no pam_wheel.so, adding...")
            write_flag = 0
            new_lines = []
            for line in lines:
                if re.match('account', line) and write_flag == 0:
                    new_lines.append('auth            required        pam_wheel.so group=wheel use_uid\n')
                    write_flag = 1
                new_lines.append(line)

            with open('/etc/pam.d/su', 'w') as write_file:
                write_file.writelines(new_lines)
        elif GROUP_EXIST == 0:
            logger.info("has pam_wheel.so but no group=wheel or use_uid, adding...")
            write_flag = 0
            new_lines = []
            for line in lines:
                if re.match('auth', line) and re.search('pam_wheel.so', line):
                    continue  # means delete this line
                elif re.match('account', line) and write_flag == 0:
                    new_lines.append('auth            required        pam_wheel.so group=wheel use_uid\n')
                    write_flag = 1
                new_lines.append(line)

            with open('/etc/pam.d/su', 'w') as write_file:
                write_file.writelines(new_lines)

        with open('/etc/pam.d/su', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('auth', line)) and\
                        re.search('pam_wheel.so', line) and re.search('group=wheel', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            logger.info("set pam.d/su, add pam_wheel.so failed,no  set option")
            Display("- Set pam.d/su, add pam_wheel.so...", "FAILED")
        else:
            logger.info("set pam.d/su, add pam_wheel.so successfully")
            Display("- Set pam.d/su, add pam_wheel.so...", "FINISHED")
    else:
        Display("- Skip forbidden user su to root due to config file...", "SKIPPING")
