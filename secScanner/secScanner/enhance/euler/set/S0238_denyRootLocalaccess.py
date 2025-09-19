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

def S0238_denyRootLocalaccess():
    InsertSection("Set prevent root users from accessing the system locally...")
    set_prevent_root_local_access = seconf.get('euler', 'set_prevent_root_local_access')
    if set_prevent_root_local_access == 'yes':
        if os.path.exists('/etc/pam.d/system-auth'):
            if not os.path.exists('/etc/pam.d/system-auth_bak'):
                shutil.copy2('/etc/pam.d/system-auth', '/etc/pam.d/system-auth_bak')
            add_bak_file('/etc/pam.d/system-auth_bak')

            pam_access_module = "pam_access.so"
            with open('/etc/pam.d/system-auth', 'r') as file:
                lines = file.readlines()

            pam_access_inserted = False
            sufficient_found = False

            for index, line in enumerate(lines):
                if 'account' in line and 'sufficient' in line and not pam_access_inserted:
                    lines.insert(index, f'account     required      {pam_access_module}\n')
                    pam_access_inserted = True
                elif pam_access_module in line:
                    pam_access_inserted = True

            with open('/etc/pam.d/system-auth', 'w') as file:
                file.writelines(lines)

            if os.path.exists('/etc/security/access.conf') and not os.path.exists('/etc/security/access.conf_bak'):
                shutil.copy2('/etc/security/access.conf', '/etc/security/access.conf_bak')
            add_bak_file('/etc/security/access.conf_bak')

            deny_tty1 = '-:root:tty1'
            tty1_exist = False
            with open('/etc/security/access.conf', 'r') as f:
                acclines = f.readlines()
                for line in acclines:
                    if (not re.match('#|$', line)) and deny_tty1 in line:
                        tty1_exist = True

            if not tty1_exist:
                with open('/etc/security/access.conf', 'a') as add_file:
                    add_file.write(deny_tty1)
                    tty1_exist = True
            else:
                with open('/etc/security/access.conf', 'w') as write_file:
                    for line in acclines:
                        write_file.write(line)

            if pam_access_inserted and tty1_exist:
                logger.info("Set prevent root users from accessing the system locally, setting ok")
                Display("- Set prevent root users from accessing the system locally...", "FINISHED")
            else:
                logger.warning("NO prevent root users from accessing the system locally set")
                Display("- NO prevent root users from accessing the system locally set...", "FAILED")

        else:
            logger.warning("file /etc/pam.d/system-auth does not exist")
            Display("- file /etc/pam.d/system-auth does not exist...", "FAILED")

    else:
        Display(f"- Skip set prevent root users from accessing the system locally...", "SKIPPING")
