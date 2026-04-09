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


def S254_gshadowProperty():
    InsertSection("Change file /etc/gshadow property...")
    gshadow_property = seconf.get('level3', 'gshadow_property')
    if gshadow_property == 'yes':
        filepath = '/etc/gshadow'
        if os.path.exists(filepath):
            # -----------------------------------------------------
            # record original property of file
            ret, result = subprocess.getstatusoutput(f'stat -c %a {filepath}')
            if ret != 0:
                logger.warning('Command execution failed')
                Display("- Command execution failed...", "FAILED")
                return
            pathlib.Path('/etc/secscanner.d/gshadow_property').touch()
            file_pro = "/etc/secscanner.d/gshadow_property"
            with open(file_pro, 'a') as add_file:
                add_file.write(f"{filepath}={result}\n")

            os.chmod(filepath, 0o0)

            logger.info("change /etc/gshadow file property successfully")
            Display("- Change /etc/gshadow property...", "FINISHED")
        else:
            Display("- file /etc/gshadow does not exist...", "SKIPPING")
    else:
        Display("- Skip change /etc/gshadow file property due to config file...", "SKIPPING")
