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
import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S21_issueRemove():
    HIDE_ISSUE_INFO = seconf.get('advance', 'hide_issue_info')
    ISVIRTUALMACHINE = get_value("ISVIRTUALMACHINE")
    InsertSection("Remove the issue.net and issue file")
    if HIDE_ISSUE_INFO == 'yes':
        if ISVIRTUALMACHINE != 1:
            if os.path.exists('/etc/issue'):
                shutil.copy2('/etc/issue', '/etc/issue_bak')
                shutil.copy2('/etc/issue.net', '/etc/issue.net_bak')
                if os.path.isfile('/etc/issue'):
                    os.remove('/etc/issue')
                if os.path.isfile('/etc/issue.net'):
                    os.remove('/etc/issue.net')
            add_bak_file('/etc/issue_bak')
            add_bak_file('/etc/issue.net_bak')

            if os.path.exists('/etc/issue'):
                logger.info("Still remain issue file, setting failed")
                Display("- Remove the issue file...", "FAILED")
            else:
                logger.info("There is no issue file remain, setting ok")
                Display("- Remove the issue file...", "FINISHED")

        else:
            logger.info("This is virtual machine, can't remove the issue file")
            Display("- This is virtual machine, can't remove the issue file", "SKIPPED")
    else:
        Display("- Skip hide issue file due to config file...", "SKIPPING")
