import os
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
logger = logging.getLogger("secscanner")


def S06_umask():
    InsertSection("Set the umask...")
    SET_UMASK = seconf.get('basic', 'set_umask')
    UMASK_VALUE = seconf.get('basic', 'umask_value')
    if SET_UMASK == 'yes':
        if not os.path.exists('/etc/profile_bak') and os.path.exists('/etc/profile'):
            shutil.copy2('/etc/profile', '/etc/profile_bak')
        if not os.path.exists('/etc/bashrc_bak') and os.path.exists('/etc/bashrc'):
            shutil.copy2('/etc/bashrc', '/etc/bashrc_bak')
        if not os.path.exists('/etc/csh.cshrc_bak') and os.path.exists('/etc/csh.cshrc'):
            shutil.copy2('/etc/csh.cshrc', '/etc/csh.cshrc_bak')
        if not os.path.exists('/etc/csh.login_bak') and os.path.exists('/etc/csh.login'):
            shutil.copy2('/etc/csh.login', '/etc/csh.login_bak')
        if not os.path.exists('/root/.bashrc_bak') and os.path.exists('/root/.bashrc'):
            shutil.copy2('/root/.bashrc', '/root/.bashrc_bak')
        if not os.path.exists('/root/.cshrc_bak') and os.path.exists('/root/.cshrc'):
            shutil.copy2('/root/.cshrc', '/root/.cshrc_bak')

        FILE = ['/etc/profile', '/etc/bashrc', '/etc/csh.cshrc', '/etc/csh.login', '/root/.bashrc', '/root/.cshrc']
        for f in FILE:
            if os.path.exists(f):
                is_exist = False
                with open (f, 'r') as read_file:
                    lines = read_file.readlines()
                    for i, line in enumerate(lines):
                        if not re.match("#|$", line) and re.search('umask', line):
                            is_exist = True
                            if re.search('umask \d+', line):
                                #lines[i] = f"umask {UMASK_VALUE}\n"
                                lines[i] = re.sub('umask \d+', f"umask {UMASK_VALUE}", line)
                            #else:
                            #    lines[i] = re.sub('umask \d+', f"umask {UMASK_VALUE}", line)
                                #lines[i] = re.sub('umask 022', f"umask {UMASK_VALUE}", line)
                            #break
                if not is_exist:
                    lines.append(f"umask {UMASK_VALUE}\n")

                with open(f, 'w') as write_file:
                    write_file.writelines(lines)

        for f in FILE:
            if os.path.exists(f):
                UMASK_RESULT = ''
                with open (f, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if (not re.match('#', line) and re.search('umask', line)):
                            temp = line.split()
                            if len(temp) == 2 and temp[1].isdigit():
                                UMASK_RESULT = temp[1]
                                if UMASK_VALUE == UMASK_RESULT:
                                    logger.info("Set the umask finished, checking ok")
                                    Display(f"- file {f} set the umask finished...", "FINISHED")
                                else:
                                    logger.info(f"Set the umask failed, the result is {UMASK_RESULT}, and is not ok")
                                    Display(f"- file {f} set the umask failed...", "FAILED")
    else:
        Display("- Skip set umask due to config file...", "SKIPPING")


