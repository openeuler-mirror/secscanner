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

def S0301_uncommonNetwork():
    set_uncommonNetwork = seconf.get('euler', 'set_uncommonNetwork')
    InsertSection("Avoid using uncommon network service...")
    if set_uncommonNetwork == 'yes':
        ret1, result1 = subprocess.getstatusoutput("modprobe -n -v sctp")
        ret2, result2 = subprocess.getstatusoutput("modprobe -n -v tipc")
        sctp_flag = False
        tipc_flag = False
        if "install /bin/true" in result1:
            sctp_flag = True
        elif "not found in directory" in result1:
            sctp_flag = True
        elif "insmod /lib/modules/" in result1:
            sctp_flag = False
        else:
            logger.error('A error occurred while checking sctp')
            Display("- A error occurred while checking sctp...", "FAILED")
            return
        if "install /bin/true" in result2:
            tipc_flag = True
        elif "not found in directory" in result2:
            tipc_flag = True
        elif "insmod /lib/modules/" in result2:
            tipc_flag = False
        else:
            logger.error('A error occurred while checking tipc')
            Display("- A error occurred while checking tipc...", "FAILED")
            return
        # display checking result
        if sctp_flag and tipc_flag:
            Display("- Already avoiding using uncommon network service...", "FINISHED")
        else:
            #fix
            with open("/etc/modprobe.d/test.conf", 'w') as write_file:
                write_file.write("install sctp /bin/true\ninstall tipc /bin/true\n")
            FLAG = False
            with open("/etc/modprobe.d/test.conf", 'r') as read_file:
                content = read_file.read()
            if content == "install sctp /bin/true\ninstall tipc /bin/true\n":
                FLAG = True
            if FLAG == True:
                logger.info("Set modprobe to avoid using sctp and tipc ok")
                Display("- Set modprobe to avoid using sctp and tipc...", "FINISHED")
            else:
                logger.warning('Set modprobe to avoid using sctp and tipc failed')
                Display("- Set modprobe to avoid using sctp and tipc failed...", "FAILED")
    else:
        Display("- Skip avoid using uncommon network service...", "SKIPPING")
