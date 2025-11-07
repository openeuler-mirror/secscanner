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
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C131_sshActive():
    InsertSection("Check if the SSH service is enabled")
    if os.path.exists('/usr/lib/systemd/system/sshd.service'):
        ret, result = subprocess.getstatusoutput(f'systemctl is-active sshd')
        if ret == 0 and result == 'active':
            flag, output = subprocess.getstatusoutput('systemctl is-enabled sshd')
            if flag == 0 and output == 'enabled':
                logger.info("SSH service enabled and running")
                Display("- SSH service enabled and running...", "OK")
            else:
                logger.info("SSH service is running but not enabled")
                Display("- SSH service is running but not enabled...", "OK")
        elif ret == 0 and result == 'inactive':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC131\n")
            logger.warning("WRN_C131_01: %s", WRN_C131_01)
            logger.warning("SUG_C131_01: %s", SUG_C131_01)
            Display("- The SSH service startup failed...", "WARNING")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC131\n")
            logger.warning("WRN_C131_02: %s", WRN_C131_02)
            logger.warning("SUG_C131_02: %s", SUG_C131_02)
            logger.warning("Failed to check if the service is available")
            Display("- Failed to check if the service is available", "WARNING")

    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC131\n")
        logger.warning("WRN_C131_03: %s", WRN_C131_03)
        logger.warning("SUG_C131_03: %s", SUG_C131_03)
        Display(f"- file /usr/lib/systemd/system/sshd.service dose not exist...", "WARNING")

