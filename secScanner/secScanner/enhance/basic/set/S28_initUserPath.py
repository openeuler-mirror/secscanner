import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S28_initUserPath():
    SET_ALWAYS_SET_PATH = seconf.get('basic', 'set_always_set_path')
    InsertSection("Set the ALWAYS_SET_PATH...")
    if SET_ALWAYS_SET_PATH == 'yes':
        if not os.path.exists('/etc/login.defs_bak'):
            shutil.copy2('/etc/login.defs', '/etc/login.defs_bak')
        add_bak_file('/etc/login.defs_bak')
        IS_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('ALWAYS_SET_PATH', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/login.defs', 'a') as add_file:
                add_file.write("\nALWAYS_SET_PATH=yes\n")
        else:
            with open('/etc/login.defs', 'w') as write_file:
                for line in lines:
                    if re.match('ALWAYS_SET_PATH', line):
                        write_file.write("ALWAYS_SET_PATH=yes\n")
                    else:
                        write_file.write(line)

        CHECK_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('ALWAYS_SET_PATH', line):
                    IS_EXIST = 1
                    temp = line.strip('\n').split('=')
                    if temp[0] == 'ALWAYS_SET_PATH' and temp[1] == 'yes':
                        CHECK_EXIST = 1
        if IS_EXIST == 0:
            logger.info("NO ALWAYS_SET_PATH set, setting failed")
            Display("- NO ALWAYS_SET_PATH set...", "FAILED")
        elif CHECK_EXIST == 0:
            logger.info("Wrong ALWAYS_SET_PATH, setting failed")
            Display("- Wrong ALWAYS_SET_PATH set...", "FAILED")
        else:
            logger.info("Has ALWAYS_SET_PATH set, setting ok")
            Display("- Set ALWAYS_SET_PATH...", "FINISHED")
    else:
        Display(f"- Skip set ALWAYS_SET_PATH due to config file...", "SKIPPING")
