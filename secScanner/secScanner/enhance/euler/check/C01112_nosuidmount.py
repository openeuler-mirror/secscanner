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

def C01112_nosuidmount():
    '''
    Function: Check whether the partitions which do not need SUID/SGID are mounted with nosuid option
    '''
    InsertSection("Check whether the partitions are mounted with nosuid option")
    default_mounts = ["/", "/sys/fs/selinux", "/proc/sys/fs/binfmt_misc", "/dev/hugepages",
                      "/boot", "/boot/efi", "/home", "/var/lib/nfs/rpc_pipefs"]
    ret, res = subprocess.getstatusoutput('mount | grep -v "nosuid" | awk -F " " \'{print $3}\'')
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
        with open(RESULT_FILE, "a", encoding="utf-8") as file:
            file.write("\nC01112\n")
        logger.warning("WRN_C01112: %s", WRN_C01112)
        logger.warning("SUG_C01112: %s", SUG_C01112)
        for mount_point in bad_mounts:
            Display("- The partition %s is not mounted with nosuid option..." % mount_point, "WARNING")
    else:
        logger.info("All the partitions which need nosuid are mounted with nosuid option, checking ok")
        Display("- Check whether the partitions are mounted with nosuid option...", "OK")
