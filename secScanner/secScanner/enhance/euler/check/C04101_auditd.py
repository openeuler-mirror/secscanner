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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C04101_auditd():
    '''
    Function: Check whether the auditd service is installed, enabled and running
    '''
    InsertSection("Check the auditd service status in your Linux System")
    ret, res = subprocess.getstatusoutput('rpm -q audit')
    ret_libs, res_libs = subprocess.getstatusoutput('rpm -q audit-libs')
    if ret != 0 or ret_libs != 0:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04101\n")
        logger.warning("WRN_C04101_01: %s", WRN_C04101_01)
        logger.warning("SUG_C04101_01: %s", SUG_C04101_01)
        Display("- The audit or audit-libs software is not installed...", "WARNING")
    else:
        logger.info(f'The status of audit software is :{res}')
        Display("- Check the audit and audit-libs software is installed...", "OK")
        ret1, res1 = subprocess.getstatusoutput('systemctl is-enabled auditd.service')
        if ret1 == 0 and res1 == 'enabled':
            logger.info(f'The status of auditd is {res1}')
            Display("- Check the auditd service is enabled...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC04101\n")
            logger.warning("WRN_C04101_02: %s", WRN_C04101_02)
            logger.warning("SUG_C04101_02: %s", SUG_C04101_02)
            Display(f"- Check the status of auditd is {res1}...", "WARNING")
        ret2, res2 = subprocess.getstatusoutput('systemctl is-active auditd.service')
        if ret2 == 0 and res2 == 'active':
            logger.info(f'The status of auditd is {res2}')
            Display("- Check the auditd service is active...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC04101\n")
            logger.warning("WRN_C04101_03: %s", WRN_C04101_03)
            logger.warning("SUG_C04101_03: %s", SUG_C04101_03)
            Display(f"- Check the status of auditd is {res2}...", "WARNING")
