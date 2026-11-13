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
import os
import shutil
import re
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def _persist_sysctl(params):
    config_file = "/etc/sysctl.d/secscanner.conf"
    if os.path.exists(config_file):
        if not os.path.exists(config_file + "_bak"):
            shutil.copy2(config_file, config_file + "_bak")
        add_bak_file(config_file + "_bak")
        with open(config_file, "r") as read_file:
            lines = read_file.readlines()
        for param, param_line in params:
            exist = False
            for line in lines:
                if re.match(param, line):
                    exist = True
                    break
            if exist:
                lines = [param_line if re.match(param, line) else line for line in lines]
            else:
                lines.append("\n" + param_line)
        with open(config_file, "w") as write_file:
            write_file.writelines(lines)
    else:
        os.makedirs("/etc/sysctl.d", exist_ok=True)
        with open(config_file, "a") as add_file:
            for param, param_line in params:
                add_file.write(param_line + "\n")

def S03516_tcptimestamps():
    '''
    Function: Set the tcp_timestamps disabled
    '''
    InsertSection("Set the tcp_timestamps disabled...")
    set_tcptimestamps = seconf.get('euler', 'set_tcptimestamps')
    if set_tcptimestamps == 'yes':
        param = 'net.ipv4.tcp_timestamps'
        result = subprocess.run(['sysctl', param], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr[-1] == '0':
            logger.info("%s already set to 0", param)
            Display("- %s has already been set to 0..." % param, "SKIPPING")
        else:
            try:
                set_result = subprocess.run(["sysctl", "-w", "%s=0" % param], capture_output=True)
            except Exception:
                os.system('sysctl -w %s=0' % param)
            if set_result.returncode == 0:
                _persist_sysctl([(param, "%s=0" % param)])
                logger.info("Set %s finish", param)
                Display("- Set %s=0..." % param, "FINISHED")
            else:
                logger.warning("Set %s failed", param)
                Display("- Set %s=0..." % param, "FAILED")
    else:
        Display("- Skip set net.ipv4.tcp_timestamps due to config file...", "SKIPPING")
