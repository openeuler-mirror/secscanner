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


def C30_ftpBanner():
    InsertSection("check the ftp banner")
    ftpBanner_set = 'unset'
    
    if os.path.exists('/etc/vsftpd/vsftpd.conf'):
        with open('/etc/vsftpd/vsftpd.conf', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('ftpd_banner', line) and not re.match('^#|^$', line):
                    ftpBanner_set = 'wrong'
                    temp = line.split('=')
                    if len(temp) == 2 and temp[1] == ('Authorized users only. All activity may be '
                                                      'monitored and reported.\n'):
                        ftpBanner_set = 'right'
        if ftpBanner_set == 'unset':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC30\n")
            logger.warning("WRN_C30_01: %s", WRN_C30_01)
            logger.warning("SUG_C30: %s", SUG_C30)
            Display("- No ftp banner config set...", "WARNING")
        elif ftpBanner_set == 'right':
            logger.info("Has ftp banner set, checking OK")
            Display("- Check the ftp banner set...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC30\n")
            logger.warning("WRN_C30_02: %s", WRN_C30_02)
            logger.warning("SUG_C30: %s", SUG_C30)
            Display("- Wrong ftp banner config set...", "WARNING")
    else:
        Display("- Path /etc/vsftpd/vsftpd.conf not exists...", "WARNING")
