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
#import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0336_delSSHpresets():
    InsertSection("Delete presets of ssh...")
    set_delSSHpresets = seconf.get('euler', 'set_delSSHpresets')
    if set_delSSHpresets == 'yes':
        ret, result = subprocess.getstatusoutput("find /home/ /root/ -name authorized_keys")
        if ret == 0 and result == '':
            logger.info("Not found ssh presets in /home/ /root/")
            Display("- Not found ssh presets in /home/ /root/...", "FINISHED")
        elif ret == 0 and "authorized_keys" in result:
            files_list = result.split("\n")
            for single_file in files_list:
                if os.path.exists(single_file):
                    os.remove(single_file)
            ret, result = subprocess.getstatusoutput("find /home/ /root/ -name authorized_keys")
            if ret == 0 and result == '':
                logger.info("Delete found ssh presets in /home/ /root/")
                Display("- Delete found ssh presets in /home/ /root/...", "FINISHED")
            else:
                logger.error("Fail to delete ssh presets in /home/ /root/")
                Display("- Fail to delete ssh presets in /home/ /root/...", "FAILED")
        else:
            logger.error("Error occured while finding ssh presets in /home/ /root/")
            Display("- Error occured while finding ssh presets in /home/ /root/...", "FAILED")
    else:
        Display("- Skip delete presets of ssh due to config file", "SKIPPING")
