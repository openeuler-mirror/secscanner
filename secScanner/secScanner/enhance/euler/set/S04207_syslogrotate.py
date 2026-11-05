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
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S04207_syslogrotate():
    set_syslogrotate = seconf.get('euler', 'set_syslogrotate')
    InsertSection("Set the rsyslog log rotate in /etc/logrotate.d/rsyslog...")
    if set_syslogrotate == 'yes':
        config_file = '/etc/logrotate.d/rsyslog'
        log_paths = ["/var/log/cron", "/var/log/maillog", "/var/log/messages", "/var/log/secure", "/var/log/spooler"]
        rotate_params = ["maxage", "rotate", "compress", "size"]
        if not os.path.exists('/etc/logrotate.d'):
            os.makedirs('/etc/logrotate.d')
        if os.path.exists(config_file):
            with open(config_file, 'r') as read_file:
                content = read_file.read()
            missing_paths = [log_path for log_path in log_paths if log_path not in content]
            missing_params = [rotate_param for rotate_param in rotate_params if not re.search(rf'^\s*{rotate_param}\b', content, re.MULTILINE)]
            if not missing_paths and not missing_params:
                logger.info("the rsyslog log rotate is already configured")
                Display("- Set the rsyslog log rotate...", "SKIPPING")
                return
            if not os.path.exists(f'{config_file}_bak'):
                shutil.copy2(config_file, f'{config_file}_bak')
            add_bak_file(f'{config_file}_bak')
        with open(config_file, 'w') as write_file:
            write_file.write('\n'.join(log_paths) + '\n')
            write_file.write('{\n')
            write_file.write('    maxage 365\n')
            write_file.write('    rotate 30\n')
            write_file.write('    notifempty\n')
            write_file.write('    compress\n')
            write_file.write('    copytruncate\n')
            write_file.write('    missingok\n')
            write_file.write('    size +4096k\n')
            write_file.write('    sharedscripts\n')
            write_file.write('    postrotate\n')
            write_file.write('        /bin/kill -HUP `cat /var/run/rsyslogd.pid 2> /dev/null` 2> /dev/null || true\n')
            write_file.write('    endscript\n')
            write_file.write('}\n')

        IS_RESULT = 1
        if os.path.exists(config_file):
            with open(config_file, 'r') as read_file:
                content = read_file.read()
            missing_paths = [log_path for log_path in log_paths if log_path not in content]
            missing_params = [rotate_param for rotate_param in rotate_params if not re.search(rf'^\s*{rotate_param}\b', content, re.MULTILINE)]
            if missing_paths or missing_params:
                IS_RESULT = 0
        else:
            IS_RESULT = 0
        if IS_RESULT == 0:
            logger.info("the rsyslog log rotate is not set correctly")
            Display("- Set the rsyslog log rotate...", "FAILED")
        else:
            logger.info("the rsyslog log rotate is set, checking ok")
            Display("- Set the rsyslog log rotate...", "FINISHED")
    else:
        Display("- Skip set the rsyslog log rotate due to config file...", "SKIPPING")
