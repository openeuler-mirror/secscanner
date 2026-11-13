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

def S04201_rsyslogd():
    set_rsyslogd = seconf.get('euler', 'set_rsyslogd')
    InsertSection("Enable and start the rsyslog service in your Linux System...")
    if set_rsyslogd == 'yes':
        ret, res = subprocess.getstatusoutput('rpm -q rsyslog')
        if ret != 0:
            logger.warning(f'The rsyslog software is not installed :{res}')
            ret_ins, res_ins = subprocess.getstatusoutput('dnf install -y rsyslog')
            if ret_ins != 0:
                ret_ins, res_ins = subprocess.getstatusoutput('yum install -y rsyslog')
            if ret_ins != 0:
                logger.error(f'Failed to install the rsyslog software :{res_ins}')
                Display("- Install the rsyslog software...", "FAILED")
                return
            logger.info("The rsyslog software is installed")
            Display("- Install the rsyslog software...", "FINISHED")
        ret1, res1 = subprocess.getstatusoutput('systemctl is-enabled rsyslog.service')
        ret2, res2 = subprocess.getstatusoutput('systemctl is-active rsyslog.service')
        if ret1 == 0 and ret2 == 0:
            logger.info(f'The rsyslog is already {res1} and {res2}')
            Display("- The rsyslog is already enabled and active...", "SKIPPING")
        else:
            ret_en, res_en = subprocess.getstatusoutput('systemctl enable rsyslog.service')
            if ret_en != 0:
                logger.error(f'Failed to enable the rsyslog :{res_en}')
                Display("- Set enable the rsyslog...", "FAILED")
                return
            ret_st, res_st = subprocess.getstatusoutput('systemctl start rsyslog.service')
            if ret_st != 0:
                logger.error(f'Failed to start the rsyslog :{res_st}')
                Display("- Set start the rsyslog...", "FAILED")
            else:
                logger.info("The rsyslog is enabled and started")
                Display("- Set enable and start the rsyslog...", "FINISHED")
    else:
        Display("- Skip set enable the rsyslog due to config file...", "SKIPPING")
