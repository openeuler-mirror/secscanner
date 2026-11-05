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
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C01111_removablemount():
    '''
    Function: Check whether the removable device partitions are mounted with nodev and noexec options
    '''
    InsertSection("Check whether the removable device partitions are mounted with nodev and noexec options")
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
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01111\n")
        logger.warning("WRN_C01111: %s", WRN_C01111)
        logger.warning("SUG_C01111: %s", SUG_C01111)
        for mount_point in bad_mounts:
            Display("- The removable device partition %s is not mounted with nodev and noexec options..." % mount_point, "WARNING")
    else:
        logger.info("All the removable device partitions are mounted with nodev and noexec options, checking ok")
        Display("- Check whether the removable device partitions are mounted with nodev and noexec options...", "OK")
