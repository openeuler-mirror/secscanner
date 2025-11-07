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


def S311_auditEnabled():
    InsertSection("set audit service enabled")
    SET_AUDIT = seconf.get('level3', 'set_audit')
    if SET_AUDIT == 'yes':
        # check status of audit
        cmd1 = "systemctl is-enabled auditd"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        if ret1 == 0 and result1 == "enabled":
            Display("- Audit service is already enabled...", "FINISHED")
        elif ret1 == 1 and result1 == "disabled":
            cmd2 = "systemctl enable auditd"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                Display("- audit service enabled...", "FINISHED")
            else:
                Display("- Failed to enable audit service...", "FAILED")
        elif ret1 == 1 and result1 == "masked":
            cmd2 = "systemctl unmask auditd"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                cmd3 = "systemctl enable auditd"
                ret3, result3 = subprocess.getstatusoutput(cmd3)
                if ret3 == 0:
                    Display("- audit service enabled...", "FINISHED")
                else:
                    Display("- Failed to enable audit service...", "FAILED")
            else:
                Display("- Service masked, failed to unmask audit service...", "FAILED")
        else:
            Display("- Failed to check audit status...", "FAILED")
    else:
        Display("- Skip set audit service due to config file...", "SKIPPING")
