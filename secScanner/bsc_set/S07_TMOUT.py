import os
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
logger = logging.getLogger("secscanner")


def S07_TMOUT():
    InsertSection("Set the TMOUT...")
    SET_TMOUT = seconf.get('basic', 'set_tmout')
    TMOUT_VALUE = seconf.get('basic', 'tmout_value')
    if SET_TMOUT == 'yes':
        if not os.path.exists('/etc/profile_bak'):
            shutil.copy2('/etc/profile', '/etc/profile_bak')
        if not os.path.exists('/etc/csh.cshrc_bak'):
            shutil.copy2('/etc/csh.cshrc', '/etc/csh.cshrc_bak')
        IS_EXIST = 0
        with open ('/etc/profile', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line) and re.search('TMOUT=', line)):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            logger.info("no TMOUT set, adding...")
            with open('/etc/profile', 'w') as write_file:
                for line in lines:
                    if re.match('export', line) and re.search('TMOUT', line):
                        pass #delete line 'export TMOUT'
                    else:
                        write_file.write(line)
            with open('/etc/profile', 'a') as add_file:
                add_file.write(f"\nTMOUT={TMOUT_VALUE}\n")
                add_file.write("export TMOUT\n")
            with open('/etc/csh.cshrc', 'a') as add_file:
                add_file.write("\nset autologout=30\n")
        else:
            logger.info("exist TMOUT set, check its value...")
            TMOUT_RESULT = ''
            with open('/etc/profile', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line) and re.search('TMOUT=', line)):
                        temp = line.strip('\n').split('=') #delete \n
                        if len(temp) == 2 and temp[1].isdigit():
                            TMOUT_RESULT = temp[1]
            if TMOUT_RESULT == TMOUT_VALUE:
                logger.info("Right TMOUT set, pass...")
            else:
                logger.info(f"Wrong TMOUT set, set it to {TMOUT_VALUE}...")
                with open('/etc/profile', 'w') as write_file:
                    for line in lines:
                        if re.match('TMOUT=', line):
                            write_file.write(f"TMOUT={TMOUT_VALUE}\n")
                        elif re.match('export', line) and re.search('TMOUT', line):
                            write_file.write(f"export TMOUT\n")
                        else:
                            write_file.write(line)

        TMOUT_RESULT = ''
        with open('/etc/profile', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line) and re.search('TMOUT=', line)):
                    temp = line.strip('\n').split('=')
                    if len(temp) == 2 and temp[1].isdigit():
                        TMOUT_RESULT = temp[1]
        if TMOUT_RESULT > '300':
            logger.info(f"Set the TMOUT failed, the result is {TMOUT_RESULT}, and is no ok")
            Display("- Set the TMOUT...", "FAILED")
        else:
            logger.info("Set the TMOUT finished, checking ok")
            Display("- Set the TMOUT...", "FINISHED")
    else:
        Display("- Skip set TMOUT due to config file...", "SKIPPING")
