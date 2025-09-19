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
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
logger = logging.getLogger("secscanner")

def S0242_activeHaveged():
    InsertSection("active haveged service...")
    active_haveged = seconf.get('euler', 'active_haveged')
    if active_haveged == 'yes':
        ret, result = subprocess.getstatusoutput('rpm -qa haveged')
        if ret == 0 and result == '':
            ret, result = subprocess.getstatusoutput('yum install haveged -y')
            if ret == 0 and result != '':
                out, output = subprocess.getstatusoutput('systemctl is-active haveged')
                if out == 0 and output == 'active':
                    logger.info("service haveged already active")
                    Display("- service haveged already active...", "FINISHED")
                elif output == 'inactive':
                    flag, res = subprocess.getstatusoutput('systemctl start haveged')
                    if flag == 0:
                        check, res = subprocess.getstatusoutput('systemctl is-active haveged')
                        if check == 0 and res == 'active':
                            logger.info("service haveged already active")
                            Display("- service haveged already active...", "FINISHED")
                        else:
                            logger.warning("Haveged activation failed")
                            Display("- Haveged activation failed...", "FAILED")
                    else:
                        logger.warning("Haveged activation failed")
                        Display("- Haveged activation failed...", "FAILED")
                else:
                    logger.warning("Haveged activation failed")
                    Display("- Haveged activation failed...", "FAILED")

            else:
                logger.warning("The installation of the software package has failed")
                Display("- The installation of the software package has failed...", "FAILED")
        elif ret == 0 and result != '':
            out, output = subprocess.getstatusoutput('systemctl is-active haveged')
            if out == 0 and output == 'active':
                logger.info("service haveged already active")
                Display("- service haveged already active...", "FINISHED")
            elif output == 'inactive':
                flag, res = subprocess.getstatusoutput('systemctl start haveged')
                if flag == 0:
                    check, res = subprocess.getstatusoutput('systemctl is-active haveged')
                    if check == 0 and res == 'active':
                        logger.info("service haveged already active")
                        Display("- service haveged already active...", "FINISHED")
                    else:
                        logger.warning("Haveged activation failed")
                        Display("- Haveged activation failed...", "FAILED")
                else:
                    logger.warning("Haveged activation failed")
                    Display("- Haveged activation failed...", "FAILED")
            else:
                logger.warning("Haveged activation failed")
                Display("- Haveged activation failed...", "FAILED")

        else:
            logger.warning("Failed to obtain the installation status of haveged")
            Display("- Failed to obtain the installation status of haveged...", "FAILED")

    else:
         Display("- Skip active haveged service due to config file...", "SKIPPING")


