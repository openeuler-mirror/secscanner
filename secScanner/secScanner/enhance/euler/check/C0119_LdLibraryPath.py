# -*- coding: utf-8 -*-

import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0119_LdLibraryPath():
    '''
    Function: Check the value of LD_LIBRARY_PATH 
    '''
    InsertSection("Check the value of LD_LIBRARY_PATH in your Linux System ")
    home_dir = os.path.expandvars('$HOME')
    # /etc/profile   ~/.bashrc   ~/.bash_profile
    config_file_list = ["/etc/profile", home_dir + "/.bashrc", home_dir + "/.bash_profile"] 
    
    for config_file in config_file_list:
        if os.path.exists(config_file):
            flag = False
            with open(config_file, "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r"^export\s+LD_LIBRARY_PATH\s*=\s*.*$", line.strip()):
                        flag = True
                        break
            if flag:
                ret, res = subprocess.getstatusoutput('echo $LD_LIBRARY_PATH')
                logger.info(f"Check set of LD_LIBRARY_PATH in {config_file} file")
                Display(f"- The value of LD_LIBRARY_PATH is {res} in {config_file} file", "OK")
            else:
                with open(RESULT_FILE, 'a') as file:
                    file.write("\nC0119\n")
                logger.warning("WRN_C0119: %s", WRN_C0119)
                logger.warning("SUG_C0119: %s", SUG_C0119)
                Display(f"- Wrong set of LD_LIBRARY_PATH in {config_file} file...", "WARNING")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0119\n")
            logger.warning(f"WRN_C0119: {config_file} {WRN_no_file}")
            logger.warning(f"SUG_C0119: {config_file} {SUG_no_file}")
            Display(f"- Config file: {config_file} not found...", "SKIPPING") 