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

def C01108_romount():
    '''
    Function: Check whether the partitions which do not need to be modified are mounted with ro option
    '''
    InsertSection("Check whether the partitions are mounted with ro option")
    mount_points = []
    if 'romount_points' in seconf.options('euler'):
        mount_points = seconf.get('euler', 'romount_points').split()
    if mount_points:
        warning_flag = False
        for mount_point in mount_points:
            ret, res = subprocess.getstatusoutput('mount | grep "%s" | grep "\\<ro\\>"' % mount_point)
            if ret == 0 and res.strip():
                logger.info("The partition %s is mounted with ro option, checking ok", mount_point)
                Display("- Check whether %s is mounted with ro option..." % mount_point, "OK")
            else:
                warning_flag = True
                logger.warning("The partition %s is not mounted with ro option", mount_point)
                Display("- Check whether %s is mounted with ro option..." % mount_point, "WARNING")
        if warning_flag:
            with open(RESULT_FILE, "a", encoding="utf-8") as file:
                file.write("\nC01108\n")
            logger.warning("WRN_C01108: %s", WRN_C01108)
            logger.warning("SUG_C01108: %s", SUG_C01108)
    else:
        logger.info("No romount point configured in the config file")
        Display("- No romount point configured in the config file...", "SKIPPING")
