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


import subprocess
import logging
import os
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0338_deprecatedSSHDopt():
    InsertSection("Set delete deprecated sshd options in sshd config file...")
    set_deprecatedSSHDopt = seconf.get('euler', 'set_deprecatedSSHDopt')
    if set_deprecatedSSHDopt == 'yes':
        ret, result = subprocess.getstatusoutput("sshd -t")
        if ret == 0 and result == '':
            logger.info("Found 0 deprecated option of sshd")
            Display("- Check found 0 deprecated option of sshd", "FINISHED")
        else:
            if os.path.exists('/etc/ssh/sshd_config'):
                if not os.path.exists('/etc/ssh/sshd_config_bak'):
                    shutil.copy2('/etc/ssh/sshd_config', '/etc/ssh/sshd_config_bak')
                add_bak_file('/etc/ssh/sshd_config_bak')
            with open('/etc/ssh/sshd_config', 'r') as read_file:
                lines = read_file.readlines()
            with open('/etc/ssh/sshd_config', 'w') as write_file:
                for line in lines:
                    if re.match("RSAAuthentication", line) or re.match("RhostsRSAAuthentication", line):
                        continue
                    else:
                        write_file.write(line)
            ret, result = subprocess.getstatusoutput("sshd -t")
            if ret == 0 and result == '':
                logger.info("Delete deprecated sshd options in sshd config file finish")
                Display("- Delete deprecated sshd options in sshd config file", "FINISHED")
            else:
                logger.warning("Delete deprecated sshd options failed")
                Display("- Delete deprecated sshd options failed", "FAILED")
    else:
        Display("- Skip delete deprecated sshd options due to config file", "SKIPPING")
