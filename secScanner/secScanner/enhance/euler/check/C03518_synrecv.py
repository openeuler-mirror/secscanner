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
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C03518_synrecv():
    '''
    Function: Check whether the SYN_RECV state queue number is right set
    '''
    InsertSection("Check whether the SYN_RECV state queue number is right set")
    result = subprocess.run(['sysctl', 'net.ipv4.tcp_max_syn_backlog'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    backlog = int(resultStr.split('=')[-1].strip())
    if backlog < 256:
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03518\n")
        logger.warning("WRN_C03518: %s", WRN_C03518)
        logger.warning("SUG_C03518: %s", SUG_C03518)
        Display("- The SYN_RECV state queue number is less than 256...", "WARNING")
    else:
        logger.info("The SYN_RECV state queue number is right set")
        Display("- Check whether the SYN_RECV state queue number is right set...", "OK")
