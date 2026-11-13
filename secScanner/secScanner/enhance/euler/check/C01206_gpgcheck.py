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


import logging
import subprocess
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C01206_gpgcheck():
    '''
    Function: Check whether the yum repository configuration enables GPG check
    '''
    InsertSection("Check whether the yum repository configuration enables GPG check")
    repos_dir = '/etc/yum.repos.d'
    if os.path.isdir(repos_dir):
        repo_files = [os.path.join(repos_dir, name) for name in os.listdir(repos_dir) if name.endswith('.repo')]
        if repo_files:
            ret, pubkey_res = subprocess.getstatusoutput('rpm -qa gpg-pubkey*')
            pubkey_installed = (ret == 0 and pubkey_res.strip() != '')
            missing_gpgcheck = []
            missing_gpgkey = []
            for repo_file in repo_files:
                has_gpgcheck = False
                has_gpgkey = False
                with open(repo_file, 'r', encoding="utf-8") as file:
                    for line in file:
                        stripped = line.strip()
                        if re.match(r'^gpgcheck[ ]*=[ ]*1', stripped, re.IGNORECASE):
                            has_gpgcheck = True
                        if re.match(r'^gpgkey', stripped, re.IGNORECASE):
                            has_gpgkey = True
                if not has_gpgcheck:
                    missing_gpgcheck.append(repo_file)
                if not has_gpgkey and not pubkey_installed:
                    missing_gpgkey.append(repo_file)
            if missing_gpgcheck or missing_gpgkey:
                with open(RESULT_FILE, "a", encoding="utf-8") as file:
                    file.write("\nC01206\n")
                logger.warning("WRN_C01206: %s", WRN_C01206)
                logger.warning("SUG_C01206: %s", SUG_C01206)
                if missing_gpgcheck:
                    logger.info(f"The repo files without gpgcheck=1: {missing_gpgcheck}")
                    Display(f"- Check the gpgcheck=1 is not set in {missing_gpgcheck}...", "WARNING")
                else:
                    logger.info(f"The repo files without gpgkey: {missing_gpgkey}")
                    Display(f"- Check the gpgkey is not set in {missing_gpgkey} and no GPG public key installed...", "WARNING")
            else:
                logger.info("All repo configuration files are set with gpgcheck=1, checking ok")
                Display("- Check all the repo configuration files are set with gpgcheck=1...", "OK")
        else:
            logger.info("No repo configuration file found in /etc/yum.repos.d")
            Display("- No repo configuration file found in /etc/yum.repos.d...", "SKIPPING")
    else:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01206\n")
        logger.warning(f"WRN_C01206: {repos_dir} {WRN_no_file}")
        logger.warning(f"SUG_C01206: {repos_dir} {SUG_no_file}")
        Display(f"- Config file: {repos_dir} not found...", "SKIPPING")
