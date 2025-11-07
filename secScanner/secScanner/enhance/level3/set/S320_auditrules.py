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
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import pathlib
logger = logging.getLogger("secscanner")

def S320_auditrules():
    InsertSection("Set audit rules...")
    SET_AUDITRULES = seconf.get('level3', 'set_auditrules')
    config_file = "/etc/audit/rules.d/audit.rules"
    if SET_AUDITRULES == 'yes':
        content = '''-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shavim -p wa -k identity
-w /etc/security/opasswd -p wa -k identity
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
-a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change
-a always,exit -F arch=b64 -S clock_settime -k time-change
-a always,exit -F arch=b32 -S clock_settime -k time-change
-w /etc/localtime -p wa -k time-change
-w /etc/sudoers -p wa -k scope
-w /etc/sudoers.d -p wa -k scope
-w /var/log/sudo.log -p wa -k actions
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-w /usr/bin/kmod -p x -k modules
-a always,exit -F arch=b64 -S finit_module -S delete_module -S init_module -k modules
-a always,exit -F arch=b32 -S finit_module -S delete_module -S init_module -k modules
-w /var/run/utmp -p wa -k session
-w /var/log/wtmp -p wa -k session
-w /var/log/btmp -p wa -k session
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale
-a always,exit -F arch=b32 -S sethostname -S setdomainname -k system-locale
-w /etc/issue -p wa -k system-locale
-w /etc/issue.net -p wa -k system-locale
-w /etc/hosts -p wa -k system-locale
-w /etc/sysconfig/network -p wa -k system-locale
-w /var/log/lastlog -p wa -k logins
-w /var/run/faillock/ -p wa -k logins
-a always,exit -F arch=b64 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
-a always,exit -F arch=b32 -S unlink -S unlinkat -S rename -S renameat -F auid>=1000 -F auid!=4294967295 -k delete
-a always,exit -F arch=b64 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chmod -S fchmod -S fchmodat -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S chown -S fchown -S fchownat -S lchown -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b32 -S setxattr -S lsetxattr -S fsetxattr -S removexattr -S lremovexattr -S fremovexattr -F auid>=1000 -F auid!=4294967295 -k perm_mod
-a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
-a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate -F exit=-EACCES -F auid>=1000 -F auid!=4294967295 -k access
-w /etc/selinux/ -p wa -k MAC-policy
-a always,exit -F arch=b64 -S mount -F auid>=500 -F auid!=4294967295 -k mounts
-a always,exit -F arch=b32 -S mount -F auid>=500 -F auid!=4294967295 -k mounts
-a always,exit -S all -F path=/usr/bin/chsh -F perm=x -F auid>=1000 -F auid!=-1 -F key=priv_cmd
'''
        if os.path.exists(config_file):
            if not os.path.exists('/etc/audit/rules.d/audit.rules_bak'):
                shutil.copy2('/etc/audit/rules.d/audit.rules', '/etc/audit/rules.d/audit.rules_bak')
            add_bak_file('/etc/audit/rules.d/audit.rules_bak')
            with open(config_file, 'w') as write_file:
                write_file.write(content)
            FLAG = False
            with open(config_file, 'r') as read_file:
                file_content = read_file.read()
            if content == file_content:
                FLAG = True
            if FLAG:
                if not os.path.exists('/var/log/sudo.log'):
                    pathlib.Path('/var/log/sudo.log').touch()
                cmd1 = "auditctl -D"
                cmd2 = "augenrules --load"
                ret1, res1 = subprocess.getstatusoutput(cmd1)
                ret2, res2 = subprocess.getstatusoutput(cmd2)
                if ret1 == 0 and ret2 == 0:
                    logger.info("audit rules set correctly")
                    Display("- audit rules set correctly...", "FINISHED")
                else:
                    logger.error("audit rules set command excute error")
                    Display("- audit rules set command excute error...", "FAILED")
            else:
                logger.error("audit rules set incorrectly")
                Display("- audit rules set incorrectly...", "FAILED")
        else:
            logger.error("Config file not found, audit.rules set incorrectly")
            Display("- Config file not found, audit.rules set failed...", "FAILED")
    else:
        Display("- Skip set audit rules due to config file...", "SKIPPING")
        

