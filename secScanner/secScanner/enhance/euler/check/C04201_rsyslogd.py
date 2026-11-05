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

def C04201_rsyslogd():
    '''
    Function: Check whether the rsyslog service is installed, enabled and running
    '''
    InsertSection("Check the rsyslog service status in your Linux System")
    ret, res = subprocess.getstatusoutput('rpm -q rsyslog')
    if ret != 0:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC04201\n")
        logger.warning("WRN_C04201_01: %s", WRN_C04201_01)
        logger.warning("SUG_C04201_01: %s", SUG_C04201_01)
        Display(f"- The status of rsyslog is :{res} not installed...", "WARNING")
    else:
        logger.info(f'The status of rsyslog is :{res}')
        Display("- Check the rsyslog software is installed...", "OK")
        ret1, res1 = subprocess.getstatusoutput('systemctl is-enabled rsyslog.service')
        if ret1 == 0 and res1 == 'enabled':
            logger.info(f'The status of rsyslog is {res1}')
            Display("- Check the rsyslog service is enabled...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC04201\n")
            logger.warning("WRN_C04201_02: %s", WRN_C04201_02)
            logger.warning("SUG_C04201_02: %s", SUG_C04201_02)
            Display(f"- Check the status of rsyslog is {res1}...", "WARNING")
        ret2, res2 = subprocess.getstatusoutput('systemctl is-active rsyslog.service')
        if ret2 == 0 and res2 == 'active':
            logger.info(f'The status of rsyslog is {res2}')
            Display("- Check the rsyslog service is active...", "OK")
        else:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC04201\n")
            logger.warning("WRN_C04201_03: %s", WRN_C04201_03)
            logger.warning("SUG_C04201_03: %s", SUG_C04201_03)
            Display(f"- Check the status of rsyslog is {res2}...", "WARNING")
