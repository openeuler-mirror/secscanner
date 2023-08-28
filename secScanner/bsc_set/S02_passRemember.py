import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib
def S02_passRemember():
    InsertSection("set password remember times")

    SET_PASSWD_REM = seconf.get('basic', 'set_password_rem')
    PASSWD_REM = seconf.get('basic', 'password_rem')
    if SET_PASSWD_REM == 'yes':
        if not os.path.exists('/etc/pam.d/system-auth_bak'):
            shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
        if not (os.path.exists('/etc/security/opasswd') and os.access('/etc/security/opasswd', os.W_OK)):
            pathlib.Path('/etc/security/opasswd').touch()
            os.chown('/etc/security/opasswd', os.geteuid(), os.geteuid())# chown root:root file
            os.chmod('/etc/security/opasswd', 600)
        if os.path.exists('/etc/security/opasswd') and os.access('/etc/security/opasswd', os.W_OK):
            Display("- create the opasswd file finished...", "FINISHED")
        else:
            Display("- Set motd banner failed...", "FAILED")

        PASSWD_REM_SET = 'unset'
        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line):
                    PASSWD_REM_SET = 'set'

        if PASSWD_REM_SET == 'set':
            with open('/etc/pam.d/system-auth', 'w') as write_file:
                for line in lines:
                    if not (re.match('password', line) and re.search('pam_unix.so', line)):
                        write_file.write(line)
                    else:
                        write_file.write(f"password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok remember={PASSWD_REM}\n")
        else:
            with open('/etc/pam.d/system-auth', 'a') as add_file:
                add_file.write(f"\npassword    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok remember={PASSWD_REM}\n")

        CHECK_SET = 'unset'
        with open('/etc/pam.d/system-auth', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match('password', line) and re.search('pam_unix.so', line) and re.search('remember=', line):
                    CHECK_SET = 'set'
                    regex = r'(?<=remember=).[0-9]*'
                    SET_VAL = re.findall(regex, line)[0]
                    if SET_VAL == PASSWD_REM:
                        CHECK_SET = 'right'

        if CHECK_SET == 'right':
            Display("- Set password remember times...", "FINISHED")
        elif CHECK_SET == 'set':
            Display("- Set password remember times...", "FAILED")
        else:
            Display("- No pam_unix.so set, please check...", "FAILED")

    else:
        Display("- Skip set opasswd rem times due to config file...", "SKIPPING")



