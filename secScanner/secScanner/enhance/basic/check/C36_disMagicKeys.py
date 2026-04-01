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


def C36_disMagicKeys():
    InsertSection("check disable magic keys")
    sysrq_set = 'unset'
    if os.path.exists('/etc/sysctl.conf'):
        with open("/etc/sysctl.conf", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('kernel.sysrq', line) and not re.match('^#|^$', line):
                    sysrq_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == '0\n':
                        sysrq_set = 'right'
        
        if sysrq_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC36\n")
            logger.warning("WRN_C36_01: %s", WRN_C36_01)
            logger.warning("SUG_C36: %s", SUG_C36)
            Display("- No disable magic keys set...", "WARNING")
        elif sysrq_set == 'right':
            logger.info("Has disable magic keys set, checking OK")
            Display("- Check disable magic keys set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC36\n")
            logger.warning("WRN_C36_02: %s", WRN_C36_02)
            logger.warning("SUG_C36: %s", SUG_C36)
            Display("- Wrong disable magic keys set...", "WARNING")
    else:
        Display("- No path /etc/sysctl.conf exists", "WARNING")
