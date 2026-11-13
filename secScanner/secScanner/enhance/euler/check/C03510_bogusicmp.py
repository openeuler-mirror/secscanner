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

def C03510_bogusicmp():
    '''
    Function: Check whether the bogus ICMP responses are ignored
    '''
    InsertSection("Check whether the bogus ICMP responses are ignored")
    result = subprocess.run(['sysctl', 'net.ipv4.icmp_ignore_bogus_error_responses'], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr[-1] != '1':
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC03510\n")
        logger.warning("WRN_C03510: %s", WRN_C03510)
        logger.warning("SUG_C03510: %s", SUG_C03510)
        Display("- The system does not ignore bogus ICMP responses...", "WARNING")
    else:
        logger.info("The system ignores bogus ICMP responses")
        Display("- Check whether the bogus ICMP responses are ignored...", "OK")
