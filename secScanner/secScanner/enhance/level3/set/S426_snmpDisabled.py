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


def S426_snmpDisabled():
    InsertSection("set snmp service disabled")
    SET_SNMP = seconf.get('level3', 'set_snmp')
    if SET_SNMP == 'yes':
        # check status of snmp
        service_name = "snmpd"
        cmd1 = f"systemctl is-active {service_name}"
        cmd2 = f"systemctl is-enabled {service_name}"
        ret1, result1 = subprocess.getstatusoutput(cmd1)
        ret2, result2 = subprocess.getstatusoutput(cmd2)
        if ret2 == 0 and result2 == "enabled":
            # disable snmp
            if ret1 == 0 and result1 == "active":
                ret1, result1 = subprocess.getstatusoutput(f"systemctl stop {service_name}")
                if ret1 == 0:
                    ret, result = subprocess.getstatusoutput(f"systemctl mask {service_name}")
                    if ret == 0:
                        Display(f"- {service_name} service masked...", "FINISHED")
                    else:
                        Display(f"- Failed to disable {service_name} service...", "FAILED")
            elif ret1 == 3 and result1 == "inactive":
                ret, result = subprocess.getstatusoutput(f"systemctl mask {service_name}")
                if ret == 0:
                    Display(f"- {service_name} service masked...", "FINISHED")
                else:
                    Display(f"- Failed to disable {service_name} service...", "FAILED")
            else:
                Display(f"- Failed to check {service_name} status...", "FAILED")
        elif ret2 == 1 and result2 in ["disabled", "masked"]:
            Display(f"- {service_name} service already disabled...", "FINISHED")
        elif ret2 == 1 and 'Failed to get unit file state' in result2:
            Display(f"- {service_name} service not exist...", "FINISHED")
        else:
            Display(f"- Failed to check {service_name} status...", "FAILED")
    else:
        Display("- Skip set snmp service due to config file...", "SKIPPING")
