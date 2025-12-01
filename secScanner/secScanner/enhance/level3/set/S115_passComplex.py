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
import shutil
import pathlib
from secScanner.commands.check_outprint import *
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def check_complex_set(keyword, minclass_val, minlen_val, ucredit_val, lcredit_val, dcredit_val, ocredit_val):
    # this function recheck /etc/pam.d/system-auth and show the results
    result = [0, 0, 0, 0, 0, 0]  # return a list as result
    with open('/etc/pam.d/system-auth', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search(keyword, line):
                if re.search(f'minclass={minclass_val}', line):
                    result[0] = 1
                if re.search(f'minlen={minlen_val}', line):
                    result[1] = 1
                if re.search(f'ucredit={ucredit_val}', line):
                    result[2] = 1
                if re.search(f'lcredit={lcredit_val}', line):
                    result[3] = 1
                if re.search(f'dcredit={dcredit_val}', line):
                    result[4] = 1
                if re.search(f'ocredit={ocredit_val}', line):
                    result[5] = 1

    if result[0] == 1 and result[1] == 1 and result[2] == 1 and result[3] == 1 and result[4] == 1 and result[5] == 1:
        Display("- Set password complex...", "FINISHED")

def S115_passComplex():
    InsertSection("set password complex")
    set_password_complex = seconf.get('level3', 'set_passComplex')
    minclass = seconf.get('level3', 'minclass')
    minlen = seconf.get('level3', 'minlen')
    ucredit = seconf.get('level3', 'ucredit')
    lcredit = seconf.get('level3', 'lcredit')
    dcredit = seconf.get('level3', 'dcredit')
    ocredit = seconf.get('level3', 'ocredit')
    file_name = '/etc/pam.d/system-auth'
    passwd_complex_set = 'unset'
    if set_password_complex == 'yes':
        if os.path.exists('/etc/pam.d/system-auth') and not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        add_bak_file('/etc/pam.d/system-auth_bak')
        with open(file_name, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwquality.so', line):
                    passwd_complex_set = 'set'
                    if (re.search(f'minclass={minclass}', line) and re.search(f'minlen={minlen}', line) and
                            re.search(f'ucredit={ucredit}', line) and re.search(f'lcredit={lcredit}', line) and
                            re.search(f'dcredit={dcredit}', line) and re.search(f'ocredit={ocredit}', line) and
                            re.search(f'enforce_for_root', line)):
                        passwd_complex_set = 'right'
        if passwd_complex_set == 'unset':  # no password complex set, add the following line before password line
            write_flag = 0
            with open(file_name, 'w') as write_file:
                for line in lines:
                    if re.match('password', line) and write_flag == 0:
                        write_file.write(
                            f'password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 '
                            f'difok=3 minclass={minclass} minlen={minlen} ucredit={ucredit} lcredit={lcredit} '
                            f'dcredit={dcredit} ocredit={ocredit} enforce_for_root\n')
                        write_file.write(line)
                        write_flag = 1
                    else:
                        write_file.write(line)
        else:
            with open(file_name, 'w') as write_file:  # have password complex set, no matter its right or wrong
                # delete that line and write the following line
                for line in lines:
                    if re.match('password', line) and re.search('pam_pwquality.so', line):
                        write_file.write(
                            f'password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 '
                            f'difok=3 minclass={minclass} minlen={minlen} ucredit={ucredit} lcredit={lcredit} '
                            f'dcredit={dcredit} ocredit={ocredit} enforce_for_root\n')
                    else:
                        write_file.write(line)
        check_complex_set('pam_pwquality.so', minclass, minlen, ucredit, lcredit, dcredit, ocredit)

    else:
        Display("- Skip set password complex due to config file...", "SKIPPING")

