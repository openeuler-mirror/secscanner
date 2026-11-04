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

def S01101_nouserfiles():
    '''
    Function: Set the owner and group of the files or directories without owner or group
    '''
    set_flag = seconf.get('euler', 'set_nouserfiles')
    InsertSection("Set the owner and group of the files or directories without owner or group...")

    if set_flag == 'yes':
        findTypes = ["nouser", "nogroup"]
        set_result = True
        for findType in findTypes:
            cmd = "find `df -l | sed -n '2,$p' | awk '{print $6}'` -xdev -%s 2>/dev/null" % findType
            ret, res = subprocess.getstatusoutput(cmd)
            if ret == 0 and res.strip():
                for path in res.strip().split('\n'):
                    ret2, res2 = subprocess.getstatusoutput('chown root:root "%s"' % path)
                    if ret2 != 0:
                        set_result = False
                        logger.warning("Set the owner and group of %s failed: %s", path, res2)
                    else:
                        logger.info("Set the owner and group of %s finished", path)
        if set_result:
            logger.info("Set the owner and group of the files or directories finished, checking ok")
            Display("- Set the owner and group of the files or directories...", "FINISHED")
        else:
            logger.warning("Set the owner and group of the files or directories failed")
            Display("- Set the owner and group of the files or directories...", "FAILED")
    else:
        Display("- Skip set the owner and group of the files or directories...", "SKIPPING")
