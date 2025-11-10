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


import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
logger = logging.getLogger("secscanner")

def S131_sshActive():
    InsertSection("Enable ssh service")
    enable_ssh = seconf.get('level3', 'enable_ssh')
    if enable_ssh == 'yes':
        
        ret, result = subprocess.getstatusoutput(f'systemctl is-active sshd')
        if ret == 0 and result == 'active':
            flag, output = subprocess.getstatusoutput('systemctl is-enabled sshd')
            if flag == 0 and output == 'enabled':
                logger.info("SSH service enabled and running")
                Display("- SSH service enabled and running...", "FINISHED")
            else:
                out, res = subprocess.getstatusoutput('systemctl enable sshd')
                if out == 0:
                    logger.info("SSH service enabled")
                    Display("- SSH service enabled...", "FINISHED")
        elif result == 'inactive':
            flag, output = subprocess.getstatusoutput(f'systemctl start sshd')
            if flag != 0:
                logger.error(f"ssh service startup failed —— {output}")
                Display("- The SSH service startup failed...", "FAILED")
            else:
                logger.info("SSH service successfully started")
                Display("- SSH service successfully started...", "FINISHED")
        else:
            logger.warning("Failed to check if the service is available")
            Display("- Failed to check if the service is available", "FAILED")

    else:
        Display("- Skip enable ssh due to config file...", "SKIPPING")

