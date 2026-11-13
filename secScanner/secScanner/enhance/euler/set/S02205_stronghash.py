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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02205_stronghash():
    '''
    Function: ensure that the password is encrypted with strong hash algorithm
    '''
    InsertSection("set that the password is encrypted with strong hash algorithm...")
    set_flag = seconf.get('euler', 'set_stronghash')
    if set_flag == 'yes':
        pam_file = '/etc/pam.d/system-auth'
        login_defs_file = '/etc/login.defs'
        libuser_file = '/etc/libuser.conf'
        pam_ok = False
        if os.path.exists(pam_file):
            with open(pam_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_unix.so', line) and re.search('sha512', line):
                        pam_ok = True
        login_defs_ok = False
        if os.path.exists(login_defs_file):
            with open(login_defs_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*ENCRYPT_METHOD\s+', line) and re.search('SHA512', line):
                        login_defs_ok = True
        libuser_ok = True
        if os.path.exists(libuser_file):
            libuser_ok = False
            with open(libuser_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*crypt_style\s*=', line) and re.search('sha512', line, re.IGNORECASE):
                        libuser_ok = True
        already_set = pam_ok and login_defs_ok and libuser_ok
        if already_set:
            logger.info("strong hash algorithm is already set")
            Display("- Already set the password strong hash algorithm...", "SKIPPING")
        else:
            if os.path.exists(pam_file):
                if not os.path.exists(pam_file + '_bak'):
                    shutil.copy2(pam_file, pam_file + '_bak')
                add_bak_file(pam_file + '_bak')
                with open(pam_file, 'r') as read_file:
                    lines = read_file.readlines()
                found = False
                new_lines = []
                for line in lines:
                    if re.match('password', line) and re.search('pam_unix.so', line):
                        found = True
                        new_line = line.replace('md5', 'sha512')
                        if 'sha512' not in new_line:
                            new_line = new_line.rstrip('\n') + ' sha512\n'
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
                if not found:
                    new_lines.append('password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok\n')
                with open(pam_file, 'w') as write_file:
                    write_file.writelines(new_lines)
            if os.path.exists(login_defs_file):
                if not os.path.exists(login_defs_file + '_bak'):
                    shutil.copy2(login_defs_file, login_defs_file + '_bak')
                add_bak_file(login_defs_file + '_bak')
                with open(login_defs_file, 'r') as read_file:
                    lines = read_file.readlines()
                is_exist = 0
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('ENCRYPT_METHOD', line):
                        is_exist = 1
                if is_exist == 0:
                    with open(login_defs_file, 'a') as add_file:
                        add_file.write('\nENCRYPT_METHOD SHA512\n')
                else:
                    with open(login_defs_file, 'w') as write_file:
                        for line in lines:
                            if (not re.match('#|$', line)) and re.search('ENCRYPT_METHOD', line):
                                write_file.write('ENCRYPT_METHOD SHA512\n')
                            else:
                                write_file.write(line)
            if os.path.exists(libuser_file):
                if not os.path.exists(libuser_file + '_bak'):
                    shutil.copy2(libuser_file, libuser_file + '_bak')
                add_bak_file(libuser_file + '_bak')
                with open(libuser_file, 'r') as read_file:
                    lines = read_file.readlines()
                is_exist = 0
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('crypt_style', line):
                        is_exist = 1
                if is_exist == 0:
                    with open(libuser_file, 'a') as add_file:
                        add_file.write('\ncrypt_style = sha512\n')
                else:
                    with open(libuser_file, 'w') as write_file:
                        for line in lines:
                            if (not re.match('#|$', line)) and re.search('crypt_style', line):
                                write_file.write('crypt_style = sha512\n')
                            else:
                                write_file.write(line)
            check_ok = False
            pam_ok = False
            if os.path.exists(pam_file):
                with open(pam_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match('password', line) and re.search('pam_unix.so', line) and re.search('sha512', line):
                            pam_ok = True
            login_defs_ok = False
            if os.path.exists(login_defs_file):
                with open(login_defs_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\s*ENCRYPT_METHOD\s+', line) and re.search('SHA512', line):
                            login_defs_ok = True
            libuser_ok = True
            if os.path.exists(libuser_file):
                libuser_ok = False
                with open(libuser_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\s*crypt_style\s*=', line) and re.search('sha512', line, re.IGNORECASE):
                            libuser_ok = True
            check_ok = pam_ok and login_defs_ok and libuser_ok
            if check_ok:
                logger.info("set the password strong hash algorithm successfully")
                Display("- Set the password strong hash algorithm...", "FINISHED")
            else:
                logger.warning("set the password strong hash algorithm failed")
                Display("- Set the password strong hash algorithm...", "FAILED")
    else:
        Display("- Skip set the password strong hash algorithm...", "SKIPPING")

