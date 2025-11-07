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
import logging
from secScanner.commands.check_outprint import *
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")



deny_times = seconf.get('euler', 'deny_times')
unlock_time = seconf.get('euler', 'unlock_time')
lock_attacking_user = seconf.get('euler', 'lock_attacking_user')

def sed_i2(a, b, file):
    str1 = ''
    str2 = ''
    str3 = ''
    num = 0
    if a == 'auth':
        str1 = 'auth'
        if b == 'required':
            str2 = 'required'
            str3 = 'pam_env.so'
            num = 1
        elif b == 'die':
            str2 = 'pam_sss.so'
            str3 = ' '
            num = 2
        elif b == 'sufficient':
            str2 = 'pam_succeed_if.so'
            str3 = ' '
            num = 3
        else:
            pass

    elif a == 'account':
        str1 = 'account'
        str2 = 'pam_unix.so'
        str3 = ' '
        num = 4
    else:
        pass
    with open(file, 'r') as r:
        lines = r.readlines()
    with open(file, 'w') as w:
        for line in lines:
            if line.strip().startswith((str1,'-'+str1)) and str2 in line and str3 in line:
            #if re.search(str1, line) and re.search(str2, line) and re.search(str3, line):
                if num == 1:
                    w.write(line)
                    w.write(f"auth        required      pam_faillock.so preauth audit deny={deny_times} even_deny_root "
                            f"unlock_time={unlock_time}\n")
                elif num == 2:
                    w.write(line)
                    w.write(f"auth        [default=die] pam_faillock.so authfail audit deny={deny_times} even_deny_root "
                            f"unlock_time={unlock_time}\n")
                elif num == 3:
                    w.write(line)
                    w.write(f"auth        sufficient    pam_faillock.so authfail audit deny={deny_times} even_deny_root "
                            f"unlock_time={unlock_time}\n")
                elif num == 4:
                    w.write(line)
                    w.write("account     required      pam_faillock.so\n")
                else:
                    w.write(line)
            else:
                w.write(line)


# delete line contains [auth( require die sufficient) account(require)]
def sed_d2(a, b, file):
    with open(file, 'r') as r:
        lines = r.readlines()
    with open(file, 'w') as w:
        for line in lines:
            if re.search('pam_faillock.so', line):
                if re.match(a, line):
                    if re.search(b, line):
                        deny_match = re.search(r'\s*deny=(\d+)', line)
                        unlock_time_match = re.search(r'\s*unlock_time=(\d+)', line)
                        deny_value = deny_match.group(1) if deny_match else None
                        unlock_time_value = unlock_time_match.group(1) if unlock_time_match else None
                        if deny_value != deny_times:
                            line = re.sub(r'deny=\d+', f'deny={deny_times}', line)
                        if unlock_time_value != unlock_time:
                            line = re.sub(r'unlock_time=\d+', f'unlock_time={unlock_time}', line)
                    else:
                        w.write(line)
                else:
                    w.write(line)
            else:
                w.write(line)


def faillock_1(file, para1, para2, para3):
    IS_EXIST = 0
    with open(file, 'r') as r:
        lines = r.readlines()
        for line in lines:
            if re.search(para1, line) and re.search(para2, line) and re.search(para3, line):
                IS_EXIST = 1
    if IS_EXIST > 0:
        sed_d2(para2, para3, file)
        sed_i2(para2, para3, file)
    else:
        sed_i2(para2, para3, file)

def set_deny():
    SYSTEM_AUTH_FILE = '/etc/pam.d/system-auth'
    PASSWORD_AUTH_FILE = '/etc/pam.d/password-auth'
    if lock_attacking_user == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2(SYSTEM_AUTH_FILE, '/etc/pam.d/system-auth_bak')
        add_bak_file('/etc/pam.d/system-auth_bak')
        if not os.path.exists('/etc/pam.d/password-auth_bak'):
            shutil.copy2(PASSWORD_AUTH_FILE, '/etc/pam.d/password-auth_bak')
        add_bak_file('/etc/pam.d/password-auth_bak')
        faillock_1(SYSTEM_AUTH_FILE, 'pam_faillock.so', 'auth', 'required')
        faillock_1(SYSTEM_AUTH_FILE, 'pam_faillock.so', 'auth', 'die')
        faillock_1(SYSTEM_AUTH_FILE, 'pam_faillock.so', 'auth', 'sufficient')
        faillock_1(SYSTEM_AUTH_FILE, 'pam_faillock.so', 'account', 'required')

        faillock_1(PASSWORD_AUTH_FILE, 'pam_faillock.so', 'auth', 'required')
        faillock_1(PASSWORD_AUTH_FILE, 'pam_faillock.so', 'auth', 'die')
        faillock_1(PASSWORD_AUTH_FILE, 'pam_faillock.so', 'auth', 'sufficient')
        faillock_1(PASSWORD_AUTH_FILE, 'pam_faillock.so', 'account', 'required')

        logger.info("Set the user login lock Deny, checking ok")
        Display("- Set user login lock ...", "FINISHED")
    else:
        Display("- Skip lock system-attacking-user due to config file...", "SKIPPING")


def S0226_loginLock():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("set user deny time and unlock time")
    if OS_ID.lower() in ['bclinux', 'openeuler']:
        if OS_DISTRO in ['21.10', '22.10', '8', '22.10U1', '22.10U2', 'v24', '24', '21.10U4', '21.10 U4', 'V25']:
            set_deny()
        else:
            logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
