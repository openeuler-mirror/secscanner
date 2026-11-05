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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01113_suidsgid():
    '''
    Function: Remove the unnecessary SUID and SGID bits of the files
    '''
    set_flag = seconf.get('euler', 'set_suidsgid')
    InsertSection("Remove the unnecessary SUID and SGID bits of the files...")

    if set_flag == 'yes':
        # 系统必需的 SUID/SGID 程序白名单，不修改
        keep_files = ['/usr/bin/su', '/usr/bin/sudo', '/usr/bin/passwd', '/usr/bin/chage',
                      '/usr/bin/gpasswd', '/usr/bin/newgrp', '/usr/bin/chsh', '/usr/bin/chfn',
                      '/usr/bin/mount', '/usr/bin/umount', '/usr/bin/pkexec', '/usr/bin/crontab',
                      '/usr/sbin/unix_chkpwd', '/usr/sbin/pam_timestamp_check']
        ret, res = subprocess.getstatusoutput("find / -type f \\( -perm -4000 -o -perm -2000 \\) 2>/dev/null")
        if ret == 0 and res.strip():
            set_result = True
            has_file = False
            for path in res.strip().split('\n'):
                if path in keep_files:
                    logger.info("The file %s is needed by the system, keep its SUID and SGID bits", path)
                    continue
                has_file = True
                chmod_result = subprocess.run(['chmod', 'u-s,g-s', path], capture_output=True)
                if chmod_result.returncode != 0:
                    set_result = False
                    logger.warning("Remove the SUID and SGID bits of %s failed", path)
                else:
                    logger.info("Remove the SUID and SGID bits of %s finished", path)
            if not has_file:
                logger.info("No file needs to remove the SUID and SGID bits")
                Display("- No file needs to remove the SUID and SGID bits...", "SKIPPING")
            elif set_result:
                logger.info("Remove the unnecessary SUID and SGID bits finished, checking ok")
                Display("- Remove the unnecessary SUID and SGID bits of the files...", "FINISHED")
            else:
                logger.warning("Remove the unnecessary SUID and SGID bits failed")
                Display("- Remove the unnecessary SUID and SGID bits of the files...", "FAILED")
        else:
            logger.info("No file with SUID or SGID bits found")
            Display("- No file with SUID or SGID bits found...", "SKIPPING")
    else:
        Display("- Skip remove the unnecessary SUID and SGID bits of the files...", "SKIPPING")
