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


import os
import logging
from secScanner.commands.check_outprint import *
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

disable_telnet = seconf.get('level3', 'disable_telnet')

def S132_disableTelnet():
    InsertSection("Disable telnet service")
    if disable_telnet == 'yes':
        ret, result = subprocess.getstatusoutput('netstat -tln | grep \':23\'')
        if ret != 0 and result == '':
            logger.info('telnet.socket is inactive')
            Display("- telnet.socket is inactive...", "FINISHED")
        else:
            flag, res = subprocess.getstatusoutput('systemctl stop telnet.socket')
            if flag != 0:
                logger.warning("Stop the telnet.socket failed")
                Display("- Stop the telnet.socket failed", "FAILED")
            else:
                en, serv_en = subprocess.getstatusoutput('systemctl is-enabled telnet.socket')
                if serv_en == 'enabled':
                    dis, serv_dis = subprocess.getstatusoutput('systemctl disable telnet.socket')
                    if dis == 0:
                        logger.info("Disable telnet.socket success")
                        Display("- Successfully disable the telnet.socket...", "FINISHED")
                elif serv_en == 'disabled':
                    logger.info("Telnet.socket not enabled")
                    Display("- Telnet.socket not enabled...", "FINISHED")
                else:
                    logger.info("Disable telnet.socket failed")
                    Display("- Disable telnet.socket failed...", "FAILED")
    else:
        Display("- Skip disable telnet.socket due to config file...", "SKIPPING")

