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


def S415_aideInstall():
    InsertSection("Install aide")
    SET_AIDE = seconf.get('level3', 'set_aide')
    if SET_AIDE == 'yes':
        # check status of aide
        cmd1 = "rpm -q aide"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        if ret1 == 0:
            if 'aide' in result1:
                Display("- aide is already installed...", "FINISHED")
        else:
            cmd2 = "yum install aide -y"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                Display("- Install aide from yum...", "FINISHED")
            else:
                Display("- Failed to install aide...", "FAILED")
    else:
        Display("- Skip install aide due to config file...", "SKIPPING")
