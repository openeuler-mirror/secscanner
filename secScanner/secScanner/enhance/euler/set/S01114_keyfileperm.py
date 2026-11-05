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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01114_keyfileperm():
    '''
    Function: Set the permissions of the key files and directories
    '''
    set_flag = seconf.get('euler', 'set_keyfileperm')
    InsertSection("Set the permissions of the key files...")

    if set_flag == 'yes':
        keyFiles = [("/etc/passwd", "0644"), ("/etc/group", "0644"), ("/etc/shadow", "0000"),
                    ("/etc/gshadow", "0000"), ("/etc/passwd-", "0644"), ("/etc/group-", "0644"),
                    ("/etc/shadow-", "0000"), ("/etc/gshadow-", "0000"), ("/etc/ssh/sshd_config", "0600")]
        set_result = True
        for keyFile, perm in keyFiles:
            if os.path.exists(keyFile):
                try:
                    os.chmod(keyFile, int(perm, 8))
                except Exception:
                    set_result = False
                    logger.warning("Set the permission of %s failed", keyFile)
                    continue
                file_permission = format(os.stat(keyFile).st_mode & 0o7777, '04o')
                if file_permission != perm:
                    set_result = False
                    logger.warning("Set the permission of %s failed", keyFile)
                else:
                    logger.info("Set the permission of %s finished", keyFile)
        if set_result:
            logger.info("Set the permissions of the key files finished, checking ok")
            Display("- Set the permissions of the key files...", "FINISHED")
        else:
            logger.warning("Set the permissions of the key files failed")
            Display("- Set the permissions of the key files...", "FAILED")
    else:
        Display("- Skip set the permissions of the key files...", "SKIPPING")
