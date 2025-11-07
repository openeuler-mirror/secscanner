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
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib
logger = logging.getLogger("secscanner")


def S0216_passRemember():
    InsertSection("set password remember times")
    SET_PASSWD_REM = seconf.get('euler', 'set_password_rem')
    PASSWD_REM = seconf.get('euler', 'password_rem')
    if SET_PASSWD_REM == 'yes':
        if not os.path.exists('/etc/pam.d/password-auth_bak'):
            shutil.copy2('/etc/pam.d/password-auth', '/etc/pam.d/password-auth_bak')
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        add_bak_file('/etc/pam.d/system-auth_bak')
        if not (os.path.exists('/etc/security/opasswd') and os.access('/etc/security/opasswd', os.W_OK)):
            pathlib.Path('/etc/security/opasswd').touch()
            os.chown('/etc/security/opasswd', os.geteuid(), os.geteuid())
            os.chmod('/etc/security/opasswd', 600)
        if os.path.exists('/etc/security/opasswd') and os.access('/etc/security/opasswd', os.W_OK):
            logger.info("create the opasswd file finished successfully")
            #Display("- create the opasswd file finished...", "FINISHED")
        else:
            logger.info("create the opasswd file failed")
            #Display("- create the opasswd file failed...", "FAILED")

        PASSWD_REM_SET1 = 'unset'
        PASSWD_REM_SET2 = 'unset'
        with open('/etc/pam.d/password-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                        and re.search(f'remember={PASSWD_REM}', line) and re.search('enforce_for_root', line):
                    PASSWD_REM_SET1 = 'set'

        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                        and re.search(f'remember={PASSWD_REM}', line) and re.search('enforce_for_root', line):
                    PASSWD_REM_SET2 = 'set'

        if PASSWD_REM_SET1 != 'set':
            with open('/etc/pam.d/password-auth', 'w') as write_file:
                for line in lines:
                    if (re.match('password', line) and re.search('sufficient', line)):
                        write_file.write(\
                                f"password    required     pam_pwhistory.so use_authok remember={PASSWD_REM} enforce_for_root\n")
                        write_file.write(line)
                    else:
                        write_file.write(line)

        if PASSWD_REM_SET2 != 'set':
            with open('/etc/pam.d/system-auth', 'w') as write_file:
                for line in lines:
                    if (re.match('password', line) and re.search('sufficient', line)):
                        write_file.write(\
                                f"password    required     pam_pwhistory.so use_authok remember={PASSWD_REM} enforce_for_root\n")
                        write_file.write(line)
                    else:
                        write_file.write(line)
        CHECK_SET1 = 'unset'
        CHECK_SET2 = 'unset'
        with open('/etc/pam.d/password-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                        and re.search(f'remember={PASSWD_REM}', line) and re.search('enforce_for_root', line):
                    CHECK_SET = 'set'
                    regex = r'(?<=remember=).[0-9]*'
                    SET_VAL = re.findall(regex, line)[0]
                    if SET_VAL == PASSWD_REM:
                        CHECK_SET1 = 'right'

        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_pwhistory.so', line) \
                        and re.search(f'remember={PASSWD_REM}', line) and re.search('enforce_for_root', line):
                    CHECK_SET = 'set'
                    regex = r'(?<=remember=).[0-9]*'
                    SET_VAL = re.findall(regex, line)[0]
                    if SET_VAL == PASSWD_REM:
                        CHECK_SET2 = 'right'
        if os.path.exists('/etc/security/opasswd') and CHECK_SET1 == 'right' and CHECK_SET2 == 'right':
            logger.info("set password remember times successfully")
            Display("- Set password remember times...", "FINISHED")
        elif os.path.exists('/etc/security/opasswd') and (CHECK_SET1 == 'set' or CHECK_SET2 == 'set'):
            logger.info("set password remember times failed, wrong setting")
            Display("- Set password remember times...", "FAILED")
        else:
            logger.info("set the password remember times failed, no set option")
            Display("- No password remember times set, please check...", "FAILED")

    else:
        Display("- Skip set opasswd rem times due to config file...", "SKIPPING")



