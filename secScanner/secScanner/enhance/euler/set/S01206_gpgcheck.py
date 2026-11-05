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
import os
import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def set_repo_gpgcheck(repo_file):
    # 为 repo 文件中未开启 gpgcheck=1 的 section 补写 gpgcheck=1，返回是否发生修改
    with open(repo_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    new_lines = []
    changed = False
    in_section = False
    section_has_gpgcheck = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            if in_section and not section_has_gpgcheck:
                new_lines.append('gpgcheck=1\n')
                changed = True
            in_section = True
            section_has_gpgcheck = False
            new_lines.append(line)
        elif in_section and re.match(r'^gpgcheck[ ]*=[ ]*1', stripped, re.IGNORECASE):
            section_has_gpgcheck = True
            new_lines.append(line)
        elif in_section and re.match(r'^gpgcheck[ ]*=', stripped, re.IGNORECASE):
            new_lines.append('gpgcheck=1\n')
            changed = True
            section_has_gpgcheck = True
        else:
            new_lines.append(line)
    if in_section and not section_has_gpgcheck:
        new_lines.append('gpgcheck=1\n')
        changed = True
    if changed:
        bak_file = repo_file + '_bak'
        if not os.path.exists(bak_file):
            shutil.copy2(repo_file, bak_file)
        add_bak_file(bak_file)
        with open(repo_file, 'w', encoding="utf-8") as file:
            file.writelines(new_lines)
    return changed

def S01206_gpgcheck():
    '''
    Function: Set gpgcheck=1 for the repo files which do not enable GPG check
    '''
    set_flag = seconf.get('euler', 'set_gpgcheck')
    InsertSection("Set gpgcheck=1 for the yum repository configuration...")
    if set_flag == 'yes':
        repos_dir = '/etc/yum.repos.d'
        if os.path.isdir(repos_dir):
            repo_files = [os.path.join(repos_dir, name) for name in sorted(os.listdir(repos_dir)) if name.endswith('.repo')]
            if repo_files:
                changed_files = []
                failed_files = []
                for repo_file in repo_files:
                    try:
                        if set_repo_gpgcheck(repo_file):
                            changed_files.append(repo_file)
                    except Exception as e:
                        logger.error(f"Error setting gpgcheck=1 for {repo_file}: {e}")
                        failed_files.append(repo_file)
                if failed_files:
                    logger.warning(f"Failed to set gpgcheck=1 for the repo files: {failed_files}")
                    Display("- Set gpgcheck=1 for the yum repository configuration...", "FAILED")
                elif changed_files:
                    logger.info(f"Set gpgcheck=1 for the repo files: {changed_files}, checking ok")
                    Display("- Set gpgcheck=1 for the yum repository configuration...", "FINISHED")
                else:
                    logger.info("All repo files are already set with gpgcheck=1, no need to fix")
                    Display("- All repo files are already set with gpgcheck=1...", "SKIPPING")
            else:
                logger.info("No repo configuration file found in /etc/yum.repos.d")
                Display("- No repo configuration file found in /etc/yum.repos.d...", "SKIPPING")
        else:
            logger.warning(f"{repos_dir} does not exist")
            Display(f"- Config file: {repos_dir} not found...", "SKIPPING")
    else:
        Display("- Skip set gpgcheck=1 for the yum repository configuration...", "SKIPPING")
