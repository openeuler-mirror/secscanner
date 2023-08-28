import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib
from secScanner.commands.check_outprint import *

def check_complex_set(keyword, minclass_val, minlen_val, ucredit_val, lcredit_val, dcredit_val, ocredit_val):
    #this function recheck /etc/pam.d/system-auth and show the results
    result = [0, 0, 0, 0, 0, 0]#return a list as result
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
    InsertSection("set password minclass")
    if result[0] == 1:
        Display("- Set password minclass finished...", "FINISHED")
    else:
        Display("- Set password minclass failed...", "FAILED")

    InsertSection("set password minlen")
    if result[1] == 1:
        Display("- Set password minlen finished...", "FINISHED")
    else:
        Display("- Set password minlen failed...", "FAILED")

    InsertSection("set password ucredit")
    if result[2] == 1:
        Display("- Set password ucredit finished...", "FINISHED")
    else:
        Display("- Set password ucredit failed...", "FAILED")

    InsertSection("set password lcredit")
    if result[3] == 1:
        Display("- Set password lcredit finished...", "FINISHED")
    else:
        Display("- Set password lcredit failed...", "FAILED")

    InsertSection("set password dcredit")
    if result[4] == 1:
        Display("- Set password dcredit finished...", "FINISHED")
    else:
        Display("- Set password dcredit failed...", "FAILED")

    InsertSection("set password ocredit")
    if result[5] == 1:
        Display("- Set password ocredit finished...", "FINISHED")
    else:
        Display("- Set password ocredit failed...", "FAILED")


def S03_passComplex():
    InsertSection("set password complex")
    SET_PASSWD_CPX = seconf.get('basic', 'set_password_rem')
    MINCLASS = seconf.get('basic', 'minclass')
    MINLEN = seconf.get('basic', 'minlen')
    UCREDIT = seconf.get('basic', 'ucredit')
    LCREDIT = seconf.get('basic', 'lcredit')
    DCREDIT = seconf.get('basic', 'dcredit')
    OCREDIT = seconf.get('basic', 'ocredit')
    FILE_NAME = '/etc/pam.d/system-auth'
    PASSWD_CPX_SET = 'unset'
    PASSWD_CPX_SET2 = 'unset'
    if SET_PASSWD_CPX == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        if OS_DISTRO == '8' or OS_DISTRO == '\"8\"' : # check pwquality line
            with open(FILE_NAME, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_pwquality.so', line):
                        PASSWD_CPX_SET = 'set'
                        if (    re.search(f'minclass={MINCLASS}', line) and re.search(f'minlen={MINLEN}', line) and
                                re.search(f'ucredit={UCREDIT}', line) and re.search(f'lcredit={LCREDIT}', line) and
                                re.search(f'dcredit={DCREDIT}', line) and re.search(f'ocredit={OCREDIT}', line) ):
                            PASSWD_CPX_SET = 'right'
            if PASSWD_CPX_SET == 'unset': # no password complex set, add the following line in target file
                with open(FILE_NAME, 'a') as add_file:
                    add_file.write(f'\npassword    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
            else:
                with open(FILE_NAME, 'w') as write_file: # have password complex set, no matter its right or wrong , delete that line and write the following line
                    for line in lines:
                        if re.match('password', line) and re.search('pam_pwquality.so', line):
                            write_file.write(f'password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
                        else:
                            write_file.write(line)
            check_complex_set('pam_pwquality.so', MINCLASS, MINLEN, UCREDIT, LCREDIT, DCREDIT, OCREDIT)
        elif OS_DISTRO == '7' or OS_DISTRO == '\"7\"' :# delete cracklib line, check pwquality line
            with open(FILE_NAME, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_pwquality.so', line):
                        PASSWD_CPX_SET = 'set'
                        if (    re.search(f'minclass={MINCLASS}', line) and re.search(f'minlen={MINLEN}', line) and
                                re.search(f'ucredit={UCREDIT}', line) and re.search(f'lcredit={LCREDIT}', line) and
                                re.search(f'dcredit={DCREDIT}', line) and re.search(f'ocredit={OCREDIT}', line) ):
                            PASSWD_CPX_SET = 'right'
                    if re.match('password', line) and re.search('pam_cracklib.so', line):
                        PASSWD_CPX_SET2 = 'set'
            if PASSWD_CPX_SET == 'unset' and PASSWD_CPX_SET2 == 'unset': #just need add pwquality line
                with open(FILE_NAME, 'a') as add_file:
                    add_file.write(f'\npassword    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
            else:
                with open(FILE_NAME, 'w') as write_file:
                    for line in lines:
                        if not( (re.match('password', line) and re.search('pam_pwquality.so', line)) or (re.match('password', line) and re.search('pam_pw_cracklib.so', line))):
                            #find line doesnt contain pwquality or cracklib
                            write_file.write(line)
                        elif re.match('password', line) and re.search('pam_pwquality.so', line):
                            write_file.write(f'password    requisite     pam_pwquality.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
                        else:
                            pass
                        # else:#this line contains cracklib, dont need to write
            check_complex_set('pam_pwquality.so', MINCLASS, MINLEN, UCREDIT, LCREDIT, DCREDIT, OCREDIT)

        elif OS_DISTRO == '6' or OS_DISTRO == '\"6\"' : #  check cracklib line
            with open(FILE_NAME, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.match('password', line) and re.search('pam_cracklib.so', line):
                        PASSWD_CPX_SET = 'set'
                        if (    re.search(f'minclass={MINCLASS}', line) and re.search(f'minlen={MINLEN}', line) and
                                re.search(f'ucredit={UCREDIT}', line) and re.search(f'lcredit={LCREDIT}', line) and
                                re.search(f'dcredit={DCREDIT}', line) and re.search(f'ocredit={OCREDIT}', line) ):
                            PASSWD_CPX_SET = 'right'
            if PASSWD_CPX_SET == 'unset': # no password complex set, add the following line in target file
                with open(FILE_NAME, 'a') as add_file:
                    add_file.write(f'\npassword    requisite     pam_cracklib.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
            else:
                with open(FILE_NAME, 'w') as write_file: # have password complex set, no matter its right or wrong , delete that line and write the following line
                    for line in lines:
                        if re.match('password', line) and re.search('pam_cracklib.so', line):
                            write_file.write(f'password    requisite     pam_cracklib.so try_first_pass local_users_only retry=3 difok=3 minclass={MINCLASS} minlen={MINLEN} ucredit={UCREDIT} lcredit={LCREDIT} dcredit={DCREDIT} ocredit={OCREDIT} authtok_type=\n')
                        else:
                            write_file.write(line)
            check_complex_set('pam_cracklib.so', MINCLASS, MINLEN, UCREDIT, LCREDIT, DCREDIT, OCREDIT)
        else:
            Display("- Skip set password complex due to config file...","SKIPPING")

    else:
        Display("- Skip set password complex due to config file...", "SKIPPING")
