import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import pathlib
logger = logging.getLogger("secscanner")


def S02_passRemember():
    InsertSection("set password remember times")
    SET_PASSWD_REM = seconf.get('basic', 'set_password_rem')
    PASSWD_REM = seconf.get('basic', 'password_rem')
    if SET_PASSWD_REM == 'yes':
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
                        write_file.write(f"password    sufficient    pam_unix.so sha512 shadow nullok try_first_pass "
                                         f"use_authtok remember={PASSWD_REM}\n")
        else:
            with open('/etc/pam.d/system-auth', 'a') as add_file:
                add_file.write(f"\npassword    sufficient    pam_unix.so sha512 shadow nullok try_first_pass "
                               f"use_authtok remember={PASSWD_REM}\n")

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
        if os.path.exists('/etc/security/opasswd') and CHECK_SET == 'right':
            logger.info("set password remember times successfully")
            Display("- Set password remember times...", "FINISHED")
        elif os.path.exists('/etc/security/opasswd') and CHECK_SET == 'set':
            logger.info("set password remember times failed, wrong setting")
            Display("- Set password remember times...", "FAILED")
        else:
            logger.info("set the password remember times failed, no set option")
            Display("- No password remember times set, please check...", "FAILED")

    else:
        Display("- Skip set opasswd rem times due to config file...", "SKIPPING")



