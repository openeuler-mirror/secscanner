import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib


def need_change_file(filepath, filepath_bak, passwd_rem):

    if os.path.exists('filepath') and not os.path.exists('filepath_bak'):
        shutil.copy2('filepath', 'filepath_bak')
    elif os.path.exists('filepath'):
        passwd_flag = 'unset'
        with open(filepath, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line):
                    passwd_flag = 'set'

        if passwd_flag == 'set':
            with open(filepath, 'w') as write_file:
                for line in lines:
                    if not (re.match('password', line) and re.search('pam_unix.so', line)):
                        write_file.write(line)
                    else:
                        write_file.write(f"password    sufficient    pam_unix.so sha256 shadow nullok "
                                         f"try_first_pass use_authtok remember={passwd_rem}\n")
        else:
            with open(filepath, 'a') as add_file:
                add_file.write(f"\npassword    sufficient    pam_unix.so sha256  shadow "
                               f"nullok try_first_pass use_authtok remember={passwd_rem}\n")

        check_set = 'unset'
        with open(filepath, 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line) and re.search('remember=', line):
                    check_set = 'set'
                    regex = r'(?<=remember=).[0-9]*'
                    set_val = re.findall(regex, line)[0]
                    if set_val == passwd_rem:
                        check_set = 'right'
    else:
        Display(f"- {filepath} not exist...", "SKIPPING")
    return check_set


def S02_passRemember():
    InsertSection("set password remember times")
    set_password_rem= seconf.get('basic', 'set_password_rem')
    password_rem = seconf.get('basic', 'password_rem')

    if set_password_rem == 'yes':
        check_set_sys_auth = need_change_file('/etc/pam.d/system-auth','/etc/pam.d/system-auth_bak',password_rem)
        check_set_passwd_auth = need_change_file('/etc/pam.d/password-auth',
                                                 '/etc/pam.d/password-auth_bak',password_rem)
        if check_set_sys_auth == 'right' and check_set_passwd_auth == 'right':
            Display("- Set password remember times...", "FINISHED")
        elif check_set_sys_auth == 'set' and check_set_passwd_auth == 'set':
            Display("- Set password remember times...", "FAILED")
        else:
            Display("- No pam_unix.so set, please check...", "FAILED")

    else:
        Display("- Skip set password remember times due to config file...", "SKIPPING")



