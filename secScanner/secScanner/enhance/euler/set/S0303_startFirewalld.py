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
import logging
import os
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0303_startFirewalld():
    InsertSection("Start firewalld...")
    set_startFirewalld = seconf.get('euler', 'set_startFirewalld')
    if set_startFirewalld == 'yes':
        ret1, result1 = subprocess.getstatusoutput("systemctl is-active firewalld")
        ret2, result2 = subprocess.getstatusoutput("systemctl is-active iptables")
        ret3, result3 = subprocess.getstatusoutput("systemctl is-active nftables")
        if result1 == "active" and result2 == "inactive" and result3 == "inactive":
            logger.info("Set firewalld active and iptables & nftables inactive ok")
            Display("- Already set firewalld active and iptables & nftables inactive...", "FINISHED")
            return
        firewalld_flag = False
        iptables_flag = False
        nftables_flag = False
        if ret1 == 0 and result1 == "active":
            firewalld_flag = True
        else:
            ret1, result1 = subprocess.getstatusoutput("systemctl start firewalld")
            if ret1 == 0:
                firewalld_flag = True
        if ret2 == 0 and result2 == "active":
            ret2, result2 = subprocess.getstatusoutput("systemctl stop iptables")
            if ret2 == 0:
                iptables_flag = True
        else:
            iptables_flag = True
        if ret3 == 0 and result3 == "active":
            ret3, result3 = subprocess.getstatusoutput("systemctl stop nftables")
            if ret3 == 0:
                nftables_flag = True
        else:
            nftables_flag = True
        if firewalld_flag and iptables_flag and nftables_flag:
            logger.info("Set firewalld active and iptables & nftables inactive ok")
            Display("- Set firewalld active and iptables & nftables inactive...", "FINISHED")
        else:
            logger.warning('Fail to Set firewalld active and iptables & nftables inactive')
            Display("- Fail to Set firewalld active and iptables & nftables inactive...", "FAILED")
    else:
        Display("- Skip set firewalld service...", "SKIPPING")
