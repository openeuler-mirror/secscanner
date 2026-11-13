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

def C01107_filesystemmod():
    '''
    Function: Check whether the unneeded filesystems are banned from being mounted
    '''
    InsertSection("Check whether the unneeded filesystems are banned from being mounted")
    filesystems = ["cramfs", "freevxfs", "jffs2", "hfs", "hfsplus", "squashfs", "udf", "vfat",
                   "fat", "msdos", "nfs", "ceph", "fuse", "overlay", "xfs"]
    warnMessage = [WRN_C01107_01, WRN_C01107_02, WRN_C01107_03, WRN_C01107_04, WRN_C01107_05,
                   WRN_C01107_06, WRN_C01107_07, WRN_C01107_08, WRN_C01107_09, WRN_C01107_10,
                   WRN_C01107_11, WRN_C01107_12, WRN_C01107_13, WRN_C01107_14, WRN_C01107_15]
    sugMessage = [SUG_C01107_01, SUG_C01107_02, SUG_C01107_03, SUG_C01107_04, SUG_C01107_05,
                  SUG_C01107_06, SUG_C01107_07, SUG_C01107_08, SUG_C01107_09, SUG_C01107_10,
                  SUG_C01107_11, SUG_C01107_12, SUG_C01107_13, SUG_C01107_14, SUG_C01107_15]

    for i in range(len(filesystems)):
        filesystem = filesystems[i]
        ret, res = subprocess.getstatusoutput("modprobe -n -v %s | grep -E '(%s|install)'" % (filesystem, filesystem))
        if ret == 0 and 'install /bin/true' in res:
            logger.info("The %s filesystem is banned from being mounted, checking ok", filesystem)
            Display("- Check whether the %s filesystem is banned from mounting..." % filesystem, "OK")
        else:
            ret2, res2 = subprocess.getstatusoutput("lsmod | grep %s" % filesystem)
            if ret != 0 and ret2 != 0:
                logger.info("The %s filesystem is not supported in the system, checking ok", filesystem)
                Display("- Check whether the %s filesystem is banned from mounting..." % filesystem, "OK")
            else:
                with open(RESULT_FILE, "a", encoding="utf-8") as file:
                    file.write("\nC01107\n")
                logger.warning("WRN_C01107_%02d: %s", (i + 1), warnMessage[i])
                logger.warning("SUG_C01107_%02d: %s", (i + 1), sugMessage[i])
                Display("- The %s filesystem is not banned from mounting..." % filesystem, "WARNING")
