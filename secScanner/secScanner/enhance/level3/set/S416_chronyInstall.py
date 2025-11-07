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


import subprocess
import shutil
import logging
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S416_chronyInstall():
    InsertSection("Install chrony")
    SET_AIDE = seconf.get('level3', 'set_chrony')
    if SET_AIDE == 'yes':
        # check status of chrony
        cmd1 = "rpm -q chrony"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        if ret1 == 0:
            if 'chrony' in result1:
                Display("- chrony is already installed...", "FINISHED")
        else:
            cmd2 = "yum install chrony -y"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                Display("- Install chrony from yum...", "FINISHED")
            else:
                Display("- Failed to install chrony...", "FAILED")
    else:
        Display("- Skip install chrony due to config file...", "SKIPPING")
