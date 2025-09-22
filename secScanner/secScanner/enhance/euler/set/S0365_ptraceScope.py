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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0365_ptraceScope():
    InsertSection("Set config of kernel.yama.ptrace_scope...")
    set_ptraceScope = seconf.get('euler', 'set_ptraceScope')
    if set_ptraceScope == 'yes':
        if os.path.exists('/etc/sysctl.conf'):
            if not os.path.exists('/etc/sysctl.conf_bak'):
                shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
            add_bak_file('/etc/sysctl.conf_bak')
            exist = False
            set = False
            try:
                with open("/etc/sysctl.conf", "r") as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match("kernel.yama.ptrace_scope", line):
                            exist = True
                            if re.search("kernel.yama.ptrace_scope=2", line):
                                set = True
                if exist and set:
                    logger.info("Check set of kernel.yama.ptrace_scope right")
                    Display("- Already right set kernel.yama.ptrace_scope in sysctl config", "FINISHED")
                    return
                if exist:
                    with open("/etc/sysctl.conf", "w") as write_file:
                        for line in lines:
                            if re.match("kernel.yama.ptrace_scope", line):
                                write_file.write("kernel.yama.ptrace_scope=2\n")
                            else:
                                write_file.write(line)
                else:
                    with open("/etc/sysctl.conf", "a") as add_file:
                        add_file.write("\nkernel.yama.ptrace_scope=2\n")
                flag = False
                with open("/etc/sysctl.conf", "r") as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.search(r"^\s*kernel\.yama\.ptrace_scope\s*=\s*2\s*$", line.strip()):                            
                            flag = True
                            break
                if flag:
                    logger.info("Set kernel.yama.ptrace_scope finish")
                    Display("- Set kernel.yama.ptrace_scope in sysctl config file", "FINISHED")
                else:
                    logger.warning("Set kernel.yama.ptrace_scope failed")
                    Display("- Set kernel.yama.ptrace_scope in sysctl config", "FAILED")
            except IOError:
                logger.warning("Set kernel.yama.ptrace_scope failed")
                Display("- Set kernel.yama.ptrace_scope in sysctl config", "FAILED")
        else:
            logger.warning("sysctl config file not exist")
            Display("- sysctl config file not exist", "FAILED")
    else:
        Display("Skip set kernel.yama.ptrace_scope due to config file...", "SKIPPING")
 