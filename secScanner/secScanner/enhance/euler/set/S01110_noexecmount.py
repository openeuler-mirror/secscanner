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

def S01110_noexecmount():
    '''
    Function: Remount the partitions which have no executable files with noexec option
    '''
    set_flag = seconf.get('euler', 'set_noexecmount')
    InsertSection("Remount the partitions with noexec option...")

    if set_flag == 'yes':
        mount_points = []
        if 'noexecmount_points' in seconf.options('euler'):
            mount_points = seconf.get('euler', 'noexecmount_points').split()
        if mount_points:
            set_result = True
            has_point = False
            for mount_point in mount_points:
                ret, res = subprocess.getstatusoutput('mount | grep "%s" | grep "noexec"' % mount_point)
                if ret == 0 and res.strip():
                    logger.info("The partition %s has already been mounted with noexec option", mount_point)
                    continue
                has_point = True
                ret2, res2 = subprocess.getstatusoutput('mount -o remount,noexec "%s"' % mount_point)
                if ret2 != 0:
                    set_result = False
                    logger.warning("Remount the partition %s with noexec option failed: %s", mount_point, res2)
                else:
                    logger.info("Remount the partition %s with noexec option finished", mount_point)
            if not has_point:
                logger.info("All the partitions are already mounted with noexec option")
                Display("- All the partitions are already mounted with noexec option...", "SKIPPING")
            elif set_result:
                logger.info("Remount the partitions with noexec option finished, checking ok")
                Display("- Remount the partitions with noexec option...", "FINISHED")
            else:
                logger.warning("Remount the partitions with noexec option failed")
                Display("- Remount the partitions with noexec option...", "FAILED")
        else:
            logger.info("No noexecmount point configured in the config file")
            Display("- No noexecmount point configured in the config file...", "SKIPPING")
    else:
        Display("- Skip remount the partitions with noexec option...", "SKIPPING")
