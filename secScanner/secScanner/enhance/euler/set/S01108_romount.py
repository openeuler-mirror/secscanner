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
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01108_romount():
    '''
    Function: Remount the partitions which do not need to be modified with ro option
    '''
    set_flag = seconf.get('euler', 'set_romount')
    InsertSection("Remount the partitions with ro option...")

    if set_flag == 'yes':
        mount_points = []
        if 'romount_points' in seconf.options('euler'):
            mount_points = seconf.get('euler', 'romount_points').split()
        if mount_points:
            set_result = True
            has_point = False
            for mount_point in mount_points:
                ret, res = subprocess.getstatusoutput('mount | grep "%s" | grep "\\<ro\\>"' % mount_point)
                if ret == 0 and res.strip():
                    logger.info("The partition %s has already been mounted with ro option", mount_point)
                    continue
                has_point = True
                ret2, res2 = subprocess.getstatusoutput('mount -o remount,ro "%s"' % mount_point)
                if ret2 != 0:
                    set_result = False
                    logger.warning("Remount the partition %s with ro option failed: %s", mount_point, res2)
                else:
                    logger.info("Remount the partition %s with ro option finished", mount_point)
            if not has_point:
                logger.info("All the partitions are already mounted with ro option")
                Display("- All the partitions are already mounted with ro option...", "SKIPPING")
            elif set_result:
                logger.info("Remount the partitions with ro option finished, checking ok")
                Display("- Remount the partitions with ro option...", "FINISHED")
            else:
                logger.warning("Remount the partitions with ro option failed")
                Display("- Remount the partitions with ro option...", "FAILED")
        else:
            logger.info("No romount point configured in the config file")
            Display("- No romount point configured in the config file...", "SKIPPING")
    else:
        Display("- Skip remount the partitions with ro option...", "SKIPPING")
