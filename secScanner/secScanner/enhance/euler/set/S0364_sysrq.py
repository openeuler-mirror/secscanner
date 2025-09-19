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

def S0364_sysrq():
    InsertSection("Set config of kernel.sysrq...")
    set_sysrq = seconf.get('euler', 'set_sysrq')
    if set_sysrq == 'yes':
        if os.path.exists('/etc/sysctl.conf'):
            if not os.path.exists('/etc/sysctl.conf_bak'):
                shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
            add_bak_file('/etc/sysctl.conf_bak')
            exist = False
            set = False
            try:
                sysrq_count = 0
                with open("/etc/sysctl.conf", "r") as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match("kernel.sysrq", line):
                            exist = True
                            sysrq_count += 1
                            if re.search("kernel.sysrq=0", line) and sysrq_count == 1:
                                set = True
                            else:
                                set = False
                
                if exist and set:
                    logger.info("Check set of kernel.sysrq right")
                    Display("- Already right set kernel.sysrq in sysctl config", "FINISHED")
                    return
                
                if exist:
                    with open("/etc/sysctl.conf", "w") as write_file:
                        # 只保留第一个kernel.sysrq配置，删除其他的
                        found_first = False
                        for line in lines:
                            if re.match("kernel.sysrq", line):
                                if not found_first:
                                    write_file.write("kernel.sysrq=0\n")
                                    found_first = True
                            else:
                                write_file.write(line)
                else:
                    with open("/etc/sysctl.conf", "a") as add_file:
                        add_file.write("\nkernel.sysrq=0\n")
                flag = False
                with open("/etc/sysctl.conf", "r") as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.search(r"^\s*kernel\.sysrq\s*=\s*0\s*$", line.strip()):
                            flag = True
                            break
                if flag:
                    logger.info("Set kernel.sysrq finish")
                    Display("- Set kernel.sysrq in sysctl config file", "FINISHED")
                else:
                    logger.warning("Set kernel.sysrq failed")
                    Display("- Set kernel.sysrq in sysctl config", "FAILED")
            except IOError:
                logger.warning("Set kernel.sysrq failed")
                Display("- Set kernel.sysrq in sysctl config", "FAILED")
        else:
            logger.warning("sysctl config file not exist")
            Display("- sysctl config file not exist", "FAILED")
    else:
        Display("Skip set kernel.sysrq due to config file...", "SKIPPING")
