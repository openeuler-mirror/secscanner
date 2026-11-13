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

def C01110_noexecmount():
    '''
    Function: Check whether the partitions which have no executable files are mounted with noexec option
    '''
    InsertSection("Check whether the partitions are mounted with noexec option")
    mount_points = []
    if 'noexecmount_points' in seconf.options('euler'):
        mount_points = seconf.get('euler', 'noexecmount_points').split()
    if mount_points:
        warning_flag = False
        for mount_point in mount_points:
            ret, res = subprocess.getstatusoutput('mount | grep "%s" | grep "noexec"' % mount_point)
            if ret == 0 and res.strip():
                logger.info("The partition %s is mounted with noexec option, checking ok", mount_point)
                Display("- Check whether %s is mounted with noexec option..." % mount_point, "OK")
            else:
                warning_flag = True
                logger.warning("The partition %s is not mounted with noexec option", mount_point)
                Display("- Check whether %s is mounted with noexec option..." % mount_point, "WARNING")
        if warning_flag:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01110\n")
            logger.warning("WRN_C01110: %s", WRN_C01110)
            logger.warning("SUG_C01110: %s", SUG_C01110)
    else:
        logger.info("No noexecmount point configured in the config file")
        Display("- No noexecmount point configured in the config file...", "SKIPPING")
