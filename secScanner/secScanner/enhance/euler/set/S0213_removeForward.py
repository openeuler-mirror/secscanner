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
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil

logger = logging.getLogger("secscanner")


def delete_file(file_path):
    try:
        os.remove(file_path)
        logger.info(f"Successfully deleted file {file_path}")
        Display(f"- Successfully deleted file {file_path}", "FINISHED")
    except FileNotFoundError:
        logger.warning(f"File {file_path} does not exist")
        Display(f"- File {file_path} does not exist", "FAILED")
    except OSError as e:
        logger.warning(f"Error deleting file {file_path}: {e.strerror}")
        Display(f"- Error deleting file {file_path}: {e.strerror}", "FAILED")

def S0213_removeForward():
    InsertSection("Remove the .forward file from the home directory")
    remove_home_forward = seconf.get('euler', 'remove_home_forward')
    count = 0
    fdel = False
    if remove_home_forward == 'yes':
        if os.path.exists('/etc/passwd'):
            ret, users = subprocess.getstatusoutput("grep -E -v '^(halt|sync|shutdown)' /etc/passwd")
            if ret == 0:
                users = [line.split(':') for line in users.strip().split('\n') if line.split(':')[6] not in ['/bin/false', '/sbin/nologin', '/usr/sbin/nologin']]
                for user in users:
                    home = user[5]
                    if os.path.isdir(home):
                        for root, dirs, files in os.walk(home):
                            if ".forward" in files:
                                for_path = os.path.join(root, ".forward")
                                delete_file(for_path)
                                fdel = True
                            else:
                                count += 1
                if count > 0 and fdel == False:
                    logger.info("The .forward file does not exist in the /home directory")
                    Display("- The .forward file does not exist in the /home directory...", "SKIPPING")
            else:
                logger.warning("Failed to obtain passwd user's home list")
                Display("- Failed to obtain passwd user's home list ...", "FAILED")

        else:
            logger.warning("file /etc/passwd does not exist")
            Display("- file /etc/passwd not exists...", "SKIPPING")

    else:
        Display("- Skip Remove the .forward file from the home directory due to config file...", "SKIPPING")
