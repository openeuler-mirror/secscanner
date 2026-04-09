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
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")


def C34_noCtrlAltDelBurstAction():
    InsertSection("check the system CtrlAltDel Burst Action")
    CONFIG_SET = 'unset'

    if not os.path.exists("/etc/systemd/system/ctrl-alt-del.target") and not os.path.exists("/usr/lib/systemd/system/ctrl-alt-del.target"):
        with open('/etc/systemd/system.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if re.match('CtrlAltDelBurstAction', line) and not re.match('^#|^$', line):
                    CONFIG_SET = 'wrong'
                    temp = line.split("=")
                    if len(temp) == 2 and temp[1] == 'none':
                        CONFIG_SET = 'right'

    if CONFIG_SET == 'unset':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC34\n")
        logger.warning("WRN_C34_01: %s", WRN_C34_01)
        logger.warning("SUG_C34: %s", SUG_C34)
        Display("- No system CtrlAltDel burst action config set...", "WARNING")
    elif CONFIG_SET == 'right':
        logger.info("Has system CtrlAltDel burst action set, checking OK")
        Display("- Check the system CtrlAltDel burst action...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC34\n")
        logger.warning("WRN_C34_02: %s", WRN_C34_02)
        logger.warning("SUG_C34: %s", SUG_C34)
        Display("- Wrong system CtrlAltDel burst action config set...", "WARNING")
