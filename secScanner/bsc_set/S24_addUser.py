import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil

def S24_addUser():
    ADV_OPTIONS = seconf.options('advance')  # search basic and show all options
    USERNAME = ''
    USERPASS = ''
    PROFILE = get_value("PROFILE")
    if ('username' in ADV_OPTIONS):
        USERNAME = seconf.get('advance', 'username')
    if ('userpass' in ADV_OPTIONS):
        USERPASS = seconf.get('advance', 'userpass')
    SET_ADD_ADTIONAL_USER = seconf.get('advance', 'add_adtional_user')
    logger = logging.getLogger("secscanner")
    PASSWD_USER = []
    with open('/etc/passwd', 'r') as read_file:
        lines = read_file.readlines()
        for line in lines:
            temp = line.split(':', -1)
            PASSWD_USER.append(temp[0])
    InsertSection(f"Add the customer user by {PROFILE}")
    if SET_ADD_ADTIONAL_USER == 'yes':
        if os.path.exists(PROFILE):
            if USERNAME != '':
                if not os.path.exists('/etc/passwd_bak'):
                    shutil.copy2('/etc/passwd', '/etc/passwd_bak')
                if not os.path.exists('/etc/shadow_bak'):
                    shutil.copy2('/etc/shadow', '/etc/shadow_bak')
                if not os.path.exists('/etc/group_bak'):
                    shutil.copy2('/etc/group', '/etc/group_bak')
                count_user = 0
                for i in PASSWD_USER:
                    if USERNAME == i:
                        count_user = count_user + 1
                if count_user > 0:
                    logger.info(f"already have {USERNAME}, no need to add")
                    Display(f"--indent 2 --text - Already have user:{USERNAME}...  --result SKIPPED --color YELLOW")
                else:
                    logger.info(f"Adding user: {USERNAME} and Password: {USERPASS}...")
                    subprocess.run(['useradd', '-p', USERPASS, USERNAME])
                    subprocess.run(['usermod', '-G', '10','-a', USERNAME])
                    Display(f"--indent 2 --text - Add user:{USERNAME} and Password: {USERPASS}...  --result FINISHED --color GREEN")
            else:
                logger.info(f"Has {PROFILE} file, but no username/userpass params...")
                Display(f"- Exist {PROFILE} file, but no username/userpass params...", "FAILED")
        else:
            logger.info(f"No {PROFILE} file, can not read username/userpass params...")
            Display(f"- No {PROFILE} file, can not get params...", "FAILED")
    else:
        Display(f"- Skip add additional user due to config file...", "SKIPPING")
