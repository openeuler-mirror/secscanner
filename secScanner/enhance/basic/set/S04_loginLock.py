import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")



deny_times = seconf.get('basic', 'deny_times')
unlock_time = seconf.get('basic', 'unlock_time')
lock_attacking_user = seconf.get('basic', 'lock_attacking_user')

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


def el7_set_deny():
    if lock_attacking_user == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        add_bak_file('/etc/pam.d/system-auth_bak')
        if not os.path.exists('/etc/pam.d/sshd_bak'):
            shutil.copy2('/etc/pam.d/sshd', '/etc/pam.d/sshd_bak')
        add_bak_file('/etc/pam.d/sshd_bak')
        PAM_TALLY_SET = 0
        PAM_TALLY_SET2 = 0
        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#', line) and re.search('pam_tally2.so', line):
                    PAM_TALLY_SET = 1

        if PAM_TALLY_SET == 0:
            with open('/etc/pam.d/system-auth', 'w') as write_file:
                for line in lines:
                    if re.match('auth', line) and re.search('pam_env.so', line):
                        write_file.write(
                            f"auth        required      pam_tally2.so deny={deny_times} onerr=fail unlock_time={unlock_time}\n")
                    write_file.write(line)
        else:
            with open('/etc/pam.d/system-auth', 'w') as write_file:
                for line in lines:
                    if re.match('auth', line) and re.search('pam_tally2.so', line):
                        write_file.write(
                            f"auth        required      pam_tally2.so deny={deny_times} onerr=fail unlock_time={unlock_time}\n")
                        continue
                    write_file.write(line)

        with open('/etc/pam.d/sshd', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#', line) and re.search('pam_tally2.so', line):
                    PAM_TALLY_SET2 = 1

        if PAM_TALLY_SET2 == 0:
            with open('/etc/pam.d/sshd', 'w') as write_file:
                for line in lines:
                    if re.match('auth', line) and re.search('pam_sepermit.so', line):
                        write_file.write(
                            f"auth        required      pam_tally2.so deny={deny_times} onerr=fail unlock_time={unlock_time}\n")
                    write_file.write(line)
        else:
            with open('/etc/pam.d/sshd', 'w') as write_file:
                for line in lines:
                    if re.match('auth', line) and re.search('pam_tally2.so', line):
                        write_file.write(
                            f"auth        required      pam_tally2.so deny={deny_times} onerr=fail unlock_time={unlock_time}\n")
                        continue
                    write_file.write(line)

        ##check part
        CHECK_DENY_1 = ''
        CHECK_DENY_2 = ''
        regex = r'(?<=deny=).[0-9]*'
        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#', line) and re.search('deny=', line):
                    temp = re.findall(regex, line)
                    if temp:
                        CHECK_DENY_1 = temp[0]

        with open('/etc/pam.d/sshd', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if not re.match('#', line) and re.search('deny=', line):
                    temp = re.findall(regex, line)
                    if temp:
                        CHECK_DENY_2 = temp[0]
        if CHECK_DENY_1 != '' and CHECK_DENY_1 <= 6:
            if CHECK_DENY_2 != '' and CHECK_DENY_2 <= 6:
                logger.info("Set the user login lock Deny, checking ok")
                Display("- Set user login lock ...", "FINISHED")
            else:
                logger.info("Set the user login lock Deny failed")
                Display("- Set user login lock ...", "FAILED")
        else:
            logger.info("Set the user login lock Deny failed")
            Display("- Set user login lock ...", "FAILED")
    else:
        Display("- Skip lock system-attacking-user due to config file...", "SKIPPING")


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


def S04_loginLock():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("set user deny time and unlock time")
    if OS_ID.lower() in [ 'bclinux', 'openeuler']:
        if OS_DISTRO in ['7']:
            el7_set_deny()
        elif OS_DISTRO in [ '21.10', '22.10', '8', '22.10U1', '22.10U2', 'v24', '24', '21.10U4']:
            set_deny()
        else:
            logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
            Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
    else:
        logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
