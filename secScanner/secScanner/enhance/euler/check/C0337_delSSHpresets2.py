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
def C0337_delSSHpresets2():
    InsertSection("Check other ssh presets in /home/ /root/")
    ret, result = subprocess.getstatusoutput("find /home/ /root/ -name known_hosts")
    if ret == 0 and result == '':
        logger.info("Not found ssh presets in /home/ /root/")
        Display("- Not found ssh presets in /home/ /root/...", "OK")
    elif ret == 0 and "known_hosts" in result:
        files_list = result.split("\n")
        files_string = ",".join(files_list)
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0337\n")
        logger.warning("WRN_C0337: %s", WRN_C0337)
        logger.warning("SUG_C0337: %s", SUG_C0337)
        Display(f"- Found ssh presets: {files_string}...", "WARNING")
    else:
        logger.error("Excute find cmd: 'find /home/ /root/ -name known_hosts' failed")
        Display("- A error occurred while checking ssh presets...", "FAILED")
