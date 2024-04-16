import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib
logger = logging.getLogger("secscanner")


def add_line(file):
    new_line = 'auth        required     pam_listfile.so item=user onerr=succeed sense=deny file=/etc/login.user.deny'
    conf_set = 'unset'
    with open(file, 'r') as read_file:
        lines = read_file.readlines() 
        for line in lines:
            if re.match('auth', line) and re.search('pam_listfile.so', line):
                conf_set = 'set'
    
    if conf_set == 'set':
        with open(file, 'w') as write_file:
            for line in lines:
                if not (re.match('auth', line) and re.search('pam_listfile.so', line)):
                    write_file.write(line)
                else:
                    write_file.write(new_line + '\n')
    else:
        first_auth = -1
        for i in range(len(lines)):
            if re.match('auth', lines[i]):
                first_auth = i
                break
        if first_auth >= 0:
            lines.insert(first_auth, new_line + '\n')
        with open(file, 'w') as w:
            w.writelines(lines)

def S35_nologinList():
    InsertSection("set list of users prohibited from logging in")
    set_nologin_list = seconf.get('basic', 'set_nologin_list')

    if set_nologin_list == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        if not os.path.exists('/etc/pam.d/password-auth_bak'):
            shutil.copy2('/etc/pam.d/password-auth', '/etc/pam.d/password-auth_bak')
        if not os.path.exists('/etc/login.user.deny'):
            pathlib.Path('/etc/login.user.deny').touch()
        
        add_line('/etc/pam.d/system-auth')
        add_line('/etc/pam.d/password-auth')

        check_flag_sys = False
        check_flag_paswd= False

        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('auth', line) and re.search('pam_listfile.so', line):
                    check_flag_sys = True

        with open('/etc/pam.d/password-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('auth', line) and re.search('pam_listfile.so', line):
                    check_flag_paswd = True

        if os.path.exists('/etc/login.user.deny'):
            if check_flag_sys and check_flag_paswd:
                logger.info("Set list of users prohibited from logging in, checking ok")
                Display("- Set list of users prohibited from login...", "FINISHED")
            else:
                logger.info("Set list of users prohibited from logging in failed")
                Display("- Set list of users prohibited from login ...", "FAILED")
        else:
            logger.info("path /etc/login.user.deny not exists")
            Display("- Set list of users prohibited from login ...", "FAILED")
    else:
        Display("- Skip list of users prohibited from logging in...", "SKIPPING")


            

