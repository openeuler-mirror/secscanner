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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C01114_keyfileperm():
    '''
    Function: Check whether the permissions of the key files and directories are minimized
    '''
    InsertSection("Check whether the permissions of the key files are minimized")
    keyFiles = [("/etc/passwd", "0644"), ("/etc/group", "0644"), ("/etc/shadow", "0000"),
                ("/etc/gshadow", "0000"), ("/etc/passwd-", "0644"), ("/etc/group-", "0644"),
                ("/etc/shadow-", "0000"), ("/etc/gshadow-", "0000"), ("/etc/ssh/sshd_config", "0600")]
    warnMessage = [WRN_C01114_01, WRN_C01114_02, WRN_C01114_03, WRN_C01114_04, WRN_C01114_05,
                   WRN_C01114_06, WRN_C01114_07, WRN_C01114_08, WRN_C01114_09]
    sugMessage = [SUG_C01114_01, SUG_C01114_02, SUG_C01114_03, SUG_C01114_04, SUG_C01114_05,
                  SUG_C01114_06, SUG_C01114_07, SUG_C01114_08, SUG_C01114_09]

    for i in range(len(keyFiles)):
        keyFile = keyFiles[i][0]
        perm = keyFiles[i][1]
        if os.path.exists(keyFile):
            file_permission = format(os.stat(keyFile).st_mode & 0o7777, '04o')
            if file_permission == perm:
                logger.info("The permission of %s is safe, checking ok", keyFile)
                Display("- Check the permission of %s..." % keyFile, "OK")
            else:
                with open(RESULT_FILE, "a", encoding="utf-8") as file:
                    file.write("\nC01114\n")
                logger.warning("WRN_C01114_%02d: %s", (i + 1), warnMessage[i])
                logger.warning("SUG_C01114_%02d: %s", (i + 1), sugMessage[i])
                Display("- The permission of %s is not safe..." % keyFile, "WARNING")
