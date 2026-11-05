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

def S03520_coredump():
    '''
    Function: Set the core dump disabled
    '''
    InsertSection("Set the core dump disabled...")
    set_coredump = seconf.get('euler', 'set_coredump')
    if set_coredump == 'yes':
        limits_file = "/etc/security/limits.conf"
        disabled = False
        if os.path.exists(limits_file):
            with open(limits_file, "r") as read_file:
                for line in read_file:
                    if re.match(r"\s*\*\s+hard\s+core\s+0\b", line):
                        disabled = True
                        break
        if disabled:
            logger.info("Core dump is already disabled in limits.conf")
            Display("- Core dump has already been disabled...", "SKIPPING")
        else:
            try:
                os.makedirs("/etc/security", exist_ok=True)
                if os.path.exists(limits_file):
                    if not os.path.exists(limits_file + "_bak"):
                        shutil.copy2(limits_file, limits_file + "_bak")
                    add_bak_file(limits_file + "_bak")
                with open(limits_file, "a") as add_file:
                    add_file.write("\n* hard core 0\n")
                set_result = subprocess.run(["sysctl", "-w", "fs.suid_dumpable=0"], capture_output=True)
                if set_result.returncode == 0:
                    _persist_sysctl([("fs.suid_dumpable", "fs.suid_dumpable=0")])
                logger.info("Set core dump disabled finish")
                Display("- Set core dump disabled...", "FINISHED")
            except Exception:
                logger.warning("Set core dump disabled failed")
                Display("- Set core dump disabled...", "FAILED")
    else:
        Display("- Skip set core dump disabled due to config file...", "SKIPPING")
