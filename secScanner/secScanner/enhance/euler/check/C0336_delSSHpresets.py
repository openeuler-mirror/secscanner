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

def C0336_delSSHpresets():
    InsertSection("Check ssh presets in /home/ /root/")
    ret, result = subprocess.getstatusoutput("find /home/ /root/ -name authorized_keys")
    if ret == 0 and result == '':
        logger.info("Not found ssh presets in /home/ /root/")
        Display("- Not found ssh presets in /home/ /root/...", "OK")
    elif ret == 0 and "authorized_keys" in result:
        files_list = result.split("\n")
        files_string = ",".join(files_list)
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0336\n")
        logger.warning("WRN_C0336: %s", WRN_C0336)
        logger.warning("SUG_C0336: %s", SUG_C0336)
        Display(f"- Found ssh presets: {files_string}...", "WARNING")
    else:
        logger.warning("Excute find cmd: 'find /home/ /root/ -name authorized_keys' failed")
        Display("- A error occurred while checking ssh presets...", "WARNING")
