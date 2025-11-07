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


def S312_rsyslogEnabled():
    InsertSection("set rsyslog service enabled")
    SET_RSYSLOG = seconf.get('level3', 'set_rsyslog')
    if SET_RSYSLOG == 'yes':
        # check status of rsyslog
        cmd1 = "systemctl is-enabled rsyslog"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        if ret1 == 0 and result1 == "enabled":
            Display("- Rsyslog service is already enabled...", "FINISHED")
        elif ret1 == 1 and result1 == "disabled":
            cmd2 = "systemctl enable rsyslog"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                Display("- rsyslog service enabled...", "FINISHED")
            else:
                Display("- Failed to enable rsyslog service...", "FAILED")
        elif ret1 == 1 and result1 == "masked":
            cmd2 = "systemctl unmask rsyslog"
            ret2, result2 = subprocess.getstatusoutput(cmd2)
            if ret2 == 0:
                cmd3 = "systemctl enable rsyslog"
                ret3, result3 = subprocess.getstatusoutput(cmd3)
                if ret3 == 0:
                    Display("- rsyslog service enabled...", "FINISHED")
                else:
                    Display("- Failed to enable rsyslog service...", "FAILED")
            else:
                Display("- Service masked, failed to unmask rsyslog service...", "FAILED")
        else:
            Display("- Failed to check rsyslog status...", "FAILED")
    else:
        Display("- Skip set rsyslog service due to config file...", "SKIPPING")
