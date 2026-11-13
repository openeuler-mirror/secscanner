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

def S04101_auditd():
    set_enable_auditd = seconf.get('euler', 'set_auditd')
    InsertSection("Enable and start the auditd service in your Linux System...")
    if set_enable_auditd == 'yes':
        ret, res = subprocess.getstatusoutput('rpm -q audit')
        if ret != 0:
            logger.warning(f'The audit software is not installed :{res}')
            ret_ins, res_ins = subprocess.getstatusoutput('dnf install -y audit audit-libs')
            if ret_ins != 0:
                ret_ins, res_ins = subprocess.getstatusoutput('yum install -y audit audit-libs')
            if ret_ins != 0:
                logger.error(f'Failed to install the audit software :{res_ins}')
                Display("- Install the audit and audit-libs software...", "FAILED")
                return
            logger.info("The audit software is installed")
            Display("- Install the audit and audit-libs software...", "FINISHED")
        ret1, res1 = subprocess.getstatusoutput('systemctl is-enabled auditd.service')
        ret2, res2 = subprocess.getstatusoutput('systemctl is-active auditd.service')
        if ret1 == 0 and ret2 == 0:
            logger.info(f'The auditd is already {res1} and {res2}')
            Display("- The auditd is already enabled and active...", "SKIPPING")
        else:
            ret_en, res_en = subprocess.getstatusoutput('systemctl enable auditd.service')
            if ret_en != 0:
                logger.error(f'Failed to enable the auditd :{res_en}')
                Display("- Set enable the auditd...", "FAILED")
                return
            ret_st, res_st = subprocess.getstatusoutput('systemctl start auditd.service')
            if ret_st != 0:
                logger.error(f'Failed to start the auditd :{res_st}')
                Display("- Set start the auditd...", "FAILED")
            else:
                logger.info("The auditd is enabled and started")
                Display("- Set enable and start the auditd...", "FINISHED")
    else:
        Display("- Skip set enable the auditd due to config file...", "SKIPPING")
