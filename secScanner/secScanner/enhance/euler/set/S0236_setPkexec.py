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
logger = logging.getLogger("secscanner")

content_to_write = """
polkit.addAdminRule(function(action, subject) {
    return ["unix-user:0"];
});
"""


def S0236_setPkexec():
    InsertSection("Set ordinary users cannot use pkexec to configure root privileges...")
    set_pkexec = seconf.get('euler', 'set_pkexec')
    if set_pkexec == 'yes':
        file_path = '/etc/polkit-1/rules.d/50-default.rules'
        if os.path.exists(file_path):
            if not os.path.exists(file_path + '_bak'):
                shutil.copy2(file_path, file_path + '_bak')
            add_bak_file(file_path + '_bak')

            exist = False
            with open(file_path, 'r') as file:
                existing_content = file.read()
                if content_to_write not in existing_content:
                    with open(file_path, 'a') as file:
                        file.write(content_to_write)

                else:
                    exist = True
                    pass
    
            with open(file_path, 'r') as file:
                existing_content = file.read()
                if content_to_write not in existing_content:
                    exist = False
                else:
                    exist = True

            if exist:
                logger.info("Set ordinary users cannot use pkexec to configure root privileges, setting ok")
                Display("- Set ordinary users cannot use pkexec to configure root privileges...", "FINISHED")

            else:
                logger.warning("NO ordinary users cannot use pkexec to configure root privileges set")
                Display("- NO ordinary users cannot use pkexec to configure root privileges set...", "FAILED")

        else:
            logger.warning("file /etc/polkit-1/rules.d/50-default.rules does not exist")
            Display("- file /etc/polkit-1/rules.d/50-default.rules does not exist...", "FAILED")
    else:
        Display(f"- Skip set  ordinary users cannot use pkexec to configure root privileges...", "SKIPPING")
