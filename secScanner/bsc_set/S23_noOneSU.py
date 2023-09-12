import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S23_noOneSU():
    SET_FORBIDDEN_SU = seconf.get('advance', 'forbidden_to_su')
    InsertSection("No one can su to root")
    if SET_FORBIDDEN_SU == 'yes':
        if os.path.exists('/etc/pam.d/su') and not os.path.exists('/etc/pam.d/su_bak'):
            shutil.copy2('/etc/pam.d/su', '/etc/pam.d/su_bak')

        IS_EXIST = 0
        USE_UID_EXIST = 0
        with open('/etc/pam.d/su', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('auth', line)) and re.search('pam_wheel.so', line):
                    IS_EXIST = 1
                    if re.search('use_uid', line):
                        USE_UID_EXIST = 1
        if IS_EXIST == 0:
            logger.info("no pam_wheel.so, adding...")
            write_flag = 0
            # find line with '^account', write 'auth ......' in front of this line
            # use write_flag to make sure only write one line
            with open('/etc/pam.d/su', 'w') as write_file:
                for line in lines:
                    if re.match('account', line) and write_flag == 0:
                        write_file.write('auth            required        pam_wheel.so group=wheel use_uid\n')
                        write_flag = 1
                        write_file.write(line)
                    else:
                        write_file.write(line)
        elif USE_UID_EXIST == 0:
            logger.info("has pam_wheel.so but no group=wheel or use_uid, adding...")
            write_flag = 0
            # find line with '^account', write 'auth ......' in front of this line
            # use write_flag to make sure only write one line
            with open('/etc/pam.d/su', 'w') as write_file:
                for line in lines:
                    if re.match('auth', line) and re.search('pam_wheel.so', line):
                        pass  # means delete this line
                    elif re.match('account', line) and write_flag == 0:
                        write_file.write('auth            required        pam_wheel.so group=wheel use_uid\n')
                        write_flag = 1
                        write_file.write(line)
                    else:
                        write_file.write(line)

        with open('/etc/pam.d/su', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('auth', line)) and re.search('pam_wheel.so', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            logger.info("set pam.d/su, add pam_wheel.so failed,no  set option")
            Display(f"- Set pam.d/su, add pam_wheel.so...", "FAILED")
        else:
            logger.info("set pam.d/su, add pam_wheel.so successfully")
            Display(f"- Set pam.d/su, add pam_wheel.so...", "FINISHED")
    else:
        Display(f"- Skip forbidden user su to root due to config file...", "SKIPPING")
