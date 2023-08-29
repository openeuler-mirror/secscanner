import os
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
def S06_umask():
    InsertSection("Set the mask...")
    logger = logging.getLogger("secscanner")
    SET_UMASK = seconf.get('basic', 'set_umask')
    UMASK_VALUE = seconf.get('basic', 'umask_value')
    if SET_UMASK == 'yes':
        if not os.path.exists('/etc/profile_bak'):
            shutil.copy2('/etc/profile', '/etc/profile_bak')
        if not os.path.exists('/etc/bashrc_bak'):
            shutil.copy2('/etc/bashrc', '/etc/bashrc_bak')
        if not os.path.exists('/etc/csh.cshrc_bak'):
            shutil.copy2('/etc/csh.cshrc', '/etc/csh.cshrc_bak')
        if not os.path.exists('/etc/csh.login_bak'):
            shutil.copy2('/etc/csh.login', '/etc/csh.login_bak')
        if not os.path.exists('/root/.bashrc_bak'):
            shutil.copy2('/root/.bashrc', '/etc/.bashrc_bak')
        if not os.path.exists('/root/.cshrc_bak'):
            shutil.copy2('/root/.cshrc', '/etc/.cshrc_bak')

        FILE = ['/etc/profile', '/etc/bashrc', '/etc/csh.cshrc', '/etc/csh.login', '/root/.bashrc', '/root/.cshrc']
        for f in FILE:
            if os.path.exists(f):
                IS_EXIST = 0
                with open (f, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if (not re.match('#|$', line) and re.search('umask', line)):
                            IS_EXIST = 1
                if IS_EXIST == 0:
                    with open(f, 'a') as add_file:
                        add_file.write(f"\numask {UMASK_VALUE}\n")
                else:
                    with open(f, 'w') as write_file:
                        for line in lines:
                            if re.search('umask 022', line):
                                write_file.write(f"umask {UMASK_VALUE}\n")
                            else:
                                write_file.write(line)
        num_file = 0
        num_umask = 0
        for f in FILE:
            if os.path.exists(f):
                UMASK_RESULT = ''
                num_file = num_file + 1
                with open (f, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if (not re.match('#', line) and re.search('umask', line)):
                            temp = line.split()
                            if len(temp) == 2 and temp[1].isdigit():
                                UMASK_RESULT = temp[1]
                                if UMASK_VALUE == UMASK_RESULT :
                                    num_umask = num_umask + 1
                if num_umask == num_file :
                    logger.info("Set the umask finished, checking ok")
                    Display("- Set the umask...", "FINISHED")
                else:
                    logger.info(f"Set the umask failed, the result is {UMASK_RESULT}, and is not ok")
                    Display("- Set the umask...", "FAILED")
    else:
        Display("- Skip set umask due to config file...", "SKIPPING")


