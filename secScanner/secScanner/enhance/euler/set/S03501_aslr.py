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

def S03501_aslr():
    '''
    Function: Set the kernel ASLR enabled
    '''
    InsertSection("Set the kernel ASLR enabled...")
    set_aslr = seconf.get('euler', 'set_aslr')
    if set_aslr == 'yes':
        result = subprocess.run(['sysctl', 'kernel.randomize_va_space'], capture_output=True)
        resultStr = result.stdout.strip().decode("utf-8")
        if resultStr[-1] == '2':
            logger.info("kernel.randomize_va_space already set to 2")
            Display("- kernel.randomize_va_space has already been set to 2...", "SKIPPING")
        else:
            try:
                set_result = subprocess.run(["sysctl", "-w", "kernel.randomize_va_space=2"], capture_output=True)
            except Exception:
                os.system('sysctl -w kernel.randomize_va_space=2')
            if set_result.returncode == 0:
                _persist_sysctl([("kernel.randomize_va_space", "kernel.randomize_va_space=2")])
                logger.info("Set kernel.randomize_va_space finish")
                Display("- Set kernel.randomize_va_space=2...", "FINISHED")
            else:
                logger.warning("Set kernel.randomize_va_space failed")
                Display("- Set kernel.randomize_va_space=2...", "FAILED")
    else:
        Display("- Skip set kernel.randomize_va_space due to config file...", "SKIPPING")
