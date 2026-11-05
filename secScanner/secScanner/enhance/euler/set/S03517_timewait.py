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

def S03517_timewait():
    '''
    Function: Set the TIME WAIT tcp fin timeout not greater than 60
    '''
    InsertSection("Set the TIME WAIT tcp fin timeout not greater than 60...")
    set_timewait = seconf.get('euler', 'set_timewait')
    if set_timewait == 'yes':
        param = 'net.ipv4.tcp_fin_timeout'
        result = subprocess.run(['sysctl', param], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        timeout = int(resultStr.split('=')[-1].strip())
        if timeout <= 60:
            logger.info("%s already set to %d", param, timeout)
            Display("- %s has already been set to %d..." % (param, timeout), "SKIPPING")
        else:
            try:
                set_result = subprocess.run(["sysctl", "-w", "%s=60" % param], capture_output=True)
            except Exception:
                os.system('sysctl -w %s=60' % param)
            if set_result.returncode == 0:
                _persist_sysctl([(param, "%s=60" % param)])
                logger.info("Set %s finish", param)
                Display("- Set %s=60..." % param, "FINISHED")
            else:
                logger.warning("Set %s failed", param)
                Display("- Set %s=60..." % param, "FAILED")
    else:
        Display("- Skip set net.ipv4.tcp_fin_timeout due to config file...", "SKIPPING")
