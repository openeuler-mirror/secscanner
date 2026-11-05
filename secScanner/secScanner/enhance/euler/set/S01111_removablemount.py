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
import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01111_removablemount():
    '''
    Function: Remount the removable device partitions with nodev and noexec options
    '''
    set_flag = seconf.get('euler', 'set_removablemount')
    InsertSection("Remount the removable device partitions with nodev and noexec options...")

    if set_flag == 'yes':
        bad_mounts = []
        with open('/proc/mounts', 'r') as read_file:
            for line in read_file:
                parts = line.split()
                if len(parts) < 4:
                    continue
                device = parts[0]
                mount_point = parts[1]
                options = parts[3].split(',')
                if not device.startswith('/dev/'):
                    continue
                device_name = os.path.basename(device)
                for name in [device_name, re.sub(r'p?\d+$', '', device_name)]:
                    removable_file = "/sys/block/%s/removable" % name
                    if os.path.exists(removable_file):
                        with open(removable_file, 'r') as rf:
                            if rf.read().strip() == '1':
                                if 'nodev' not in options or 'noexec' not in options:
                                    bad_mounts.append(mount_point)
                        break
        if bad_mounts:
            set_result = True
            for mount_point in bad_mounts:
                ret, res = subprocess.getstatusoutput('mount -o remount,nodev,noexec "%s"' % mount_point)
                if ret != 0:
                    set_result = False
                    logger.warning("Remount the removable device partition %s failed: %s", mount_point, res)
                else:
                    logger.info("Remount the removable device partition %s finished", mount_point)
            if set_result:
                logger.info("Remount the removable device partitions finished, checking ok")
                Display("- Remount the removable device partitions with nodev and noexec options...", "FINISHED")
            else:
                logger.warning("Remount the removable device partitions failed")
                Display("- Remount the removable device partitions with nodev and noexec options...", "FAILED")
        else:
            logger.info("All the removable device partitions are already mounted with nodev and noexec options")
            Display("- All the removable device partitions are already mounted with nodev and noexec options...", "SKIPPING")
    else:
        Display("- Skip remount the removable device partitions...", "SKIPPING")
