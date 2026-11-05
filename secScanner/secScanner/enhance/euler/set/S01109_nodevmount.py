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

def S01109_nodevmount():
    '''
    Function: Remount the partitions which do not need to mount devices with nodev option
    '''
    set_flag = seconf.get('euler', 'set_nodevmount')
    InsertSection("Remount the partitions with nodev option...")

    if set_flag == 'yes':
        default_mounts = ["/dev", "/dev/pts", "/", "/sys/fs/selinux", "/proc/sys/fs/binfmt_misc",
                          "/dev/hugepages", "/boot", "/var/lib/nfs/rpc_pipefs", "/boot/efi", "/home"]
        ret, res = subprocess.getstatusoutput('mount | grep -v "nodev" | awk -F " " \'{print $3}\'')
        bad_mounts = []
        if ret == 0 and res.strip():
            for line in res.strip().split('\n'):
                mount_point = line.strip()
                if not mount_point:
                    continue
                mount_point = mount_point.rstrip('/') or '/'
                if mount_point not in default_mounts:
                    bad_mounts.append(mount_point)
        if bad_mounts:
            set_result = True
            for mount_point in bad_mounts:
                ret2, res2 = subprocess.getstatusoutput('mount -o remount,nodev "%s"' % mount_point)
                if ret2 != 0:
                    set_result = False
                    logger.warning("Remount the partition %s with nodev option failed: %s", mount_point, res2)
                else:
                    logger.info("Remount the partition %s with nodev option finished", mount_point)
            if set_result:
                logger.info("Remount the partitions with nodev option finished, checking ok")
                Display("- Remount the partitions with nodev option...", "FINISHED")
            else:
                logger.warning("Remount the partitions with nodev option failed")
                Display("- Remount the partitions with nodev option...", "FAILED")
        else:
            logger.info("All the partitions are already mounted with nodev option")
            Display("- All the partitions are already mounted with nodev option...", "SKIPPING")
    else:
        Display("- Skip remount the partitions with nodev option...", "SKIPPING")
