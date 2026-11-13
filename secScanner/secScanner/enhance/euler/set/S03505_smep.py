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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S03505_smep():
    '''
    Function: Set the kernel SMEP enabled
    '''
    InsertSection("Set the kernel SMEP enabled...")
    set_smep = seconf.get('euler', 'set_smep')
    if set_smep == 'yes':
        with open("/proc/cpuinfo", "r") as read_file:
            cpuStr = read_file.read()
        if "smep" not in cpuStr.split():
            logger.info("The CPU does not support SMEP, skip this set")
            Display("- The CPU does not support SMEP, skip this set...", "SKIPPING")
        else:
            with open("/proc/cmdline", "r") as read_file:
                cmdStr = read_file.read()
            if not re.search("nosmep", cmdStr, re.IGNORECASE):
                logger.info("The kernel SMEP is already enabled")
                Display("- The kernel SMEP has already been enabled...", "SKIPPING")
            else:
                grub_files = ["/boot/efi/EFI/openEuler/grub.cfg",
                              "/boot/grub2/grub.cfg",
                              "/boot/grub/grub.cfg"]
                updated = False
                for grub_file in grub_files:
                    if os.path.exists(grub_file):
                        if not os.path.exists(grub_file + "_bak"):
                            shutil.copy2(grub_file, grub_file + "_bak")
                        add_bak_file(grub_file + "_bak")
                        with open(grub_file, "r") as read_file:
                            lines = read_file.readlines()
                        lines = [re.sub(r"(?i)\s*nosmep\b", "", line) for line in lines]
                        with open(grub_file, "w") as write_file:
                            write_file.writelines(lines)
                        updated = True
                if updated:
                    logger.info("Remove nosmep boot option finish")
                    Display("- Remove nosmep boot option from grub config...", "FINISHED")
                else:
                    logger.warning("Grub config file not found")
                    Display("- Remove nosmep boot option from grub config...", "FAILED")
    else:
        Display("- Skip set kernel SMEP due to config file...", "SKIPPING")
