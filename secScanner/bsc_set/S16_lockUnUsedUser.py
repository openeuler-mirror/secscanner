import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
def S16_lockUnUsedUser():
    SET_DISABLE_UNUSED_USER = seconf.get('basic', 'disable_unused_user')
    UNUSED_USER_VALUE = seconf.get('basic', 'unused_user_value').split()
    InsertSection("Lock the unused users...")
    if SET_DISABLE_UNUSED_USER == 'yes':
        if not os.path.exists('/etc/ssh/sshd_config_bak'):
            shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
        for i in UNUSED_USER_VALUE:
            print(f"lock user: {i}")
            subprocess.run(['usermod', '-L', '-s', '/bin/false', i])
        Display(f"- Use 'usermod' to lock the unused user, and change the shell...", "FINISHED")
    else:
        Display(f"- Skip lock the unused users, due to config file...", "SKIPPING")