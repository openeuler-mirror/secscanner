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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S01107_filesystemmod():
    '''
    Function: Ban the unneeded filesystems from being mounted
    '''
    set_flag = seconf.get('euler', 'set_filesystemmod')
    InsertSection("Ban the unneeded filesystems from being mounted...")

    if set_flag == 'yes':
        filesystems = ["cramfs", "freevxfs", "jffs2", "hfs", "hfsplus", "squashfs", "udf", "vfat",
                       "fat", "msdos", "nfs", "ceph", "fuse", "overlay", "xfs"]
        modprobe_conf = '/etc/modprobe.d/secscanner.conf'
        if not os.path.exists('/etc/modprobe.d'):
            os.makedirs('/etc/modprobe.d')
        if os.path.exists(modprobe_conf):
            if not os.path.exists(modprobe_conf + '_bak'):
                shutil.copy2(modprobe_conf, modprobe_conf + '_bak')
            add_bak_file(modprobe_conf + '_bak')

        set_result = True
        for filesystem in filesystems:
            ret, res = subprocess.getstatusoutput("modprobe -n -v %s | grep -E '(%s|install)'" % (filesystem, filesystem))
            if ret == 0 and 'install /bin/true' in res:
                logger.info("The %s filesystem has already been banned from being mounted", filesystem)
                continue
            with open(modprobe_conf, 'a') as add_file:
                add_file.write("install %s /bin/true\n" % filesystem)
            ret2, res2 = subprocess.getstatusoutput("lsmod | grep %s" % filesystem)
            if ret2 == 0 and res2.strip():
                remove_result = subprocess.run(['modprobe', '-r', filesystem], capture_output=True)
                if remove_result.returncode != 0:
                    set_result = False
                    logger.warning("Remove the %s filesystem failed", filesystem)
                else:
                    logger.info("Remove the %s filesystem finished", filesystem)

        conf_result = True
        with open(modprobe_conf, 'r') as read_file:
            conf_lines = read_file.readlines()
        for filesystem in filesystems:
            exist = False
            for line in conf_lines:
                if re.search(r'install\s+%s\s+/bin/true' % filesystem, line):
                    exist = True
            if not exist:
                conf_result = False
        os.chown(modprobe_conf, 0, 0)
        os.chmod(modprobe_conf, 0o600)

        if set_result and conf_result:
            logger.info("Ban the unneeded filesystems finished, checking ok")
            Display("- Ban the unneeded filesystems from being mounted...", "FINISHED")
        else:
            logger.warning("Ban the unneeded filesystems failed")
            Display("- Ban the unneeded filesystems from being mounted...", "FAILED")
    else:
        Display("- Skip ban the unneeded filesystems...", "SKIPPING")
