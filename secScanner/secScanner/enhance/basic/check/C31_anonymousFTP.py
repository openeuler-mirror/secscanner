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
import os
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")


def C31_anonymousFTP():
    InsertSection("check the prohibit anonymous FTP")
    anonymous_set = 'unset'

    if os.path.exists('/etc/vsftpd/vsftpd.conf'):
        with open('/etc/vsftpd/vsftpd.conf', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('anonymous_enable', line) and not re.match('^#|^$', line):
                    anonymous_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == 'NO\n':
                        anonymous_set = 'right'

        if anonymous_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC31\n")
            logger.warning("WRN_C31_01: %s", WRN_C31_01)
            logger.warning("SUG_C31: %s", SUG_C31)
            Display("- No prohibit anonymous FTP config set...", "WARNING")
        elif anonymous_set == 'right':
            logger.info("Has prohibit anonymous FTP set, checking OK")
            Display("- Check the prohibit anonymous FTP set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC31\n")
            logger.warning("WRN_C31_02: %s", WRN_C31_02)
            logger.warning("SUG_C31: %s", SUG_C31)
            Display("- Wrong prohibit anonymous FTP config set...", "WARNING")
    else:
        Display("- Path /etc/vsftpd/vsftpd.conf not exists...", "WARNING")

