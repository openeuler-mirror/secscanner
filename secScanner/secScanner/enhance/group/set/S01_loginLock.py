import re
import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")


#1.(1)身份鉴别②3)通过对不成功的鉴别尝试进行预先定义,并明确规定达到该值时采取的措施来实现鉴别失败的处理。

deny_times = seconf.get('basic', 'deny_times')
unlock_time = seconf.get('basic', 'unlock_time')
lock_attacking_user = seconf.get('basic', 'lock_attacking_user')

def el7_set_deny():
    if lock_attacking_user == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak') and os.path.exists('/etc/pam.d/system-auth'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        if not os.path.exists('/etc/pam.d/sshd_bak') and os.path.exists('/etc/pam.d/sshd'):
            shutil.copy2('/etc/pam.d/sshd', '/etc/pam.d/sshd_bak')
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


def S01_loginLock():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("set user deny time and unlock time")
    if OS_ID.lower() == 'bclinux' and OS_DISTRO == '7':
        el7_set_deny()
    else:
        logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")
