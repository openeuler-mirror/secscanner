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
import shutil
import re
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S03504_smap():
    '''
    Function: Set the kernel SMAP enabled
    '''
    InsertSection("Set the kernel SMAP enabled...")
    set_smap = seconf.get('euler', 'set_smap')
    if set_smap == 'yes':
        grub_file = "/boot/efi/EFI/openEuler/grub.cfg"
        if os.path.exists(grub_file):
            with open(grub_file, "r") as read_file:
                lines = read_file.readlines()
            changed = False
            new_lines = []
            for line in lines:
                if re.search("nosmap", line, re.IGNORECASE):
                    new_lines.append(re.sub("nosmap", "", line, flags=re.IGNORECASE))
                    changed = True
                else:
                    new_lines.append(line)
            if changed:
                if not os.path.exists(grub_file + "_bak"):
                    shutil.copy2(grub_file, grub_file + "_bak")
                add_bak_file(grub_file + "_bak")
                with open(grub_file, "w") as write_file:
                    write_file.writelines(new_lines)
                logger.info("Remove nosmap from grub.cfg finish")
                Display("- Remove nosmap from grub.cfg...", "FINISHED")
            else:
                logger.info("nosmap not found in grub.cfg")
                Display("- nosmap not found in grub.cfg...", "SKIPPING")
        else:
            logger.warning("grub.cfg not exist")
            Display("- grub.cfg not exist...", "FAILED")
    else:
        Display("- Skip set kernel SMAP due to config file...", "SKIPPING")
