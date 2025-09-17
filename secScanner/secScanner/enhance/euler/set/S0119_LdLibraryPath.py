# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''


import os
import logging
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")

def S0119_LdLibraryPath():
    '''
    Function: Remove the value of LD_LIBRARY_PATH 
    '''
    set_remove_LdLibraryPath = seconf.get('euler', 'set_remove_LdLibraryPath')
    InsertSection("Remove the value of LD_LIBRARY_PATH ")    
    if set_remove_LdLibraryPath == 'yes':
        home_dir = os.path.expandvars('$HOME')
        # /etc/profile   ~/.bashrc   ~/.bash_profile
        config_file_list = ["/etc/profile", home_dir + "/.bashrc", home_dir + "/.bash_profile"] 
        
        for config_file in config_file_list:
            if os.path.exists(config_file):
                if not os.path.exists(config_file + "_bak"):
                    shutil.copy2(config_file, config_file + "_bak")
                add_bak_file(config_file + "_bak")
                exist = False
                set = False
                try:
                    with open(config_file, "r") as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.match(r"^export\s+LD_LIBRARY_PATH\s*=\s*.*$", line.strip()):
                                exist = True
                                if re.search(r"^export\s+LD_LIBRARY_PATH\s*=\s*/home/\s*$", line.strip()):
                                    set = True
                    if exist and set:
                        logger.info("Check set of LD_LIBRARY_PATH right")
                        Display(f"- Already right set LD_LIBRARY_PATH in {config_file} file", "FINISHED")
                        continue
                    if exist:
                        with open(config_file, "w") as write_file:
                            for line in lines:
                                if re.match(r"^export\s+LD_LIBRARY_PATH\s*=\s*.*$", line.strip()):
                                    write_file.write("export LD_LIBRARY_PATH=/home/\n")
                                else:
                                    write_file.write(line)
                    else:
                        with open(config_file, "a") as add_file:
                            add_file.write("\nexport LD_LIBRARY_PATH=/home/\n")
                    flag = False
                    with open(config_file, "r") as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.search(r"^export\s+LD_LIBRARY_PATH\s*=\s*/home/\s*$", line.strip()):
                                flag = True
                                break
                    if flag:
                        logger.info("Set LD_LIBRARY_PATH finish")
                        Display(f"- Set LD_LIBRARY_PATH in {config_file} file", "FINISHED")
                    else:
                        logger.warning("Set LD_LIBRARY_PATH failed")
                        Display(f"- Set LD_LIBRARY_PATH in {config_file} file", "FAILED")
                except IOError:
                    logger.warning("Set LD_LIBRARY_PATH failed")
                    Display(f"- Set LD_LIBRARY_PATH in {config_file} file", "FAILED")
            else:
                logger.warning(f"{config_file} file not exist")
                Display(f"- {config_file} file not exist", "FAILED")
    else:
        Display("- Skip set remove the value of LD_LIBRARY_PATH...", "SKIPPING")
    