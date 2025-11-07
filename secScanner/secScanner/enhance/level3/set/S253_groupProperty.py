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


import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
import pathlib
logger = logging.getLogger("secscanner")


def S253_groupProperty():
    InsertSection("Change file /etc/group property...")
    group_property = seconf.get('level3', 'group_property')
    if group_property == 'yes':
        filepath = '/etc/group'
        filebak = filepath + '_bak'
        if os.path.exists(filepath):
            if not os.path.exists(filebak):
                shutil.copy2(filepath, filebak)
            add_bak_file(filebak)
            # -----------------------------------------------------
            # record original property of file
            pathlib.Path('/etc/secscanner.d/group_property').touch()
            file_pro = "/etc/secscanner.d/group_property"
            ret, result = subprocess.getstatusoutput(f'stat -c %a {filepath}')
            if ret != 0:
                logger.warning('Command execution failed')
                Display("- Command execution failed...", "FAILED")
            if not os.path.exists(filebak):
                with open(file_pro, 'a') as add_file:
                    add_file.write(f"{filepath}={result}\n")

            os.chmod(filepath, 0o644)

            logger.info("change /etc/group file property successfully")
            Display("- Change /etc/group property...", "FINISHED")
        else:
            Display("- file /etc/group does not exist...", "SKIPPING")
    else:
        Display("- Skip change /etc/group file property due to config file...", "SKIPPING")
