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

def S0346_kptrRestrict():
    InsertSection("Set config of kernel.dmesg_restrict...")
    set_kptrRestrict = seconf.get('euler', 'set_kptrRestrict')
    if set_kptrRestrict == 'yes':
        if os.path.exists('/etc/sysctl.conf'):
            if not os.path.exists('/etc/sysctl.conf_bak'):
                shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
            add_bak_file('/etc/sysctl.conf_bak')
            exist = False
            set = False
            with open("/etc/sysctl.conf", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("kernel.kptr_restrict", line):
                        exist = True
                        if re.search("kernel.kptr_restrict=1", line):
                            set = True
            if exist and set:
                logger.info("Check set of kernel.kptr_restrict right")
                Display("- Already right set kernel.kptr_restrict in sysctl config", "FINISHED")
                return
            if exist:
                with open("/etc/sysctl.conf", "w") as write_file:
                    for line in lines:
                        if re.match("kernel.kptr_restrict", line):
                            write_file.write("kernel.kptr_restrict=1\n")
                        else:
                            write_file.write(line)
            else:
                with open("/etc/sysctl.conf", "a") as add_file:
                    add_file.write("\nkernel.kptr_restrict=1\n")
            flag = False
            with open("/etc/sysctl.conf", "r") as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match("kernel.kptr_restrict=1", line):
                        flag = True
                        break
            if flag:
                logger.info("Set kernel.kptr_restrict finish")
                Display("- Set kernel.kptr_restrict in sysctl config file", "FINISHED")
            else:
                logger.warning("Set kernel.kptr_restrict failed")
                Display("- Set kernel.kptr_restrict in sysctl config", "FAILED")
        else:
            logger.warning("sysctl config file not exist")
            Display("- sysctl config file not exist", "FAILED")
    else:
        Display("Skip set kernel.kptr_restrict due to config file...", "SKIPPING")
