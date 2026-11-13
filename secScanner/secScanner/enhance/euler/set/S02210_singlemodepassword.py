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
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02210_singlemodepassword():
    '''
    Function: ensure that single user mode is protected with a password
    '''
    InsertSection("set single user mode password protection...")
    set_flag = seconf.get('euler', 'set_singlemodepassword')
    if set_flag == 'yes':
        service_items = [
            ['/usr/lib/systemd/system/rescue.service', 'ExecStart=-/usr/lib/systemd/systemd-sulogin-shell rescue'],
            ['/usr/lib/systemd/system/emergency.service', 'ExecStart=-/usr/lib/systemd/systemd-sulogin-shell emergency']
        ]
        already_set = True
        for service_file, exec_line in service_items:
            if not os.path.exists(service_file):
                already_set = False
            else:
                item_ok = False
                with open(service_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\s*ExecStart', line) and '/systemd-sulogin-shell' in line:
                            item_ok = True
                if not item_ok:
                    already_set = False
        if already_set:
            logger.info("single user mode password protection is already set")
            Display("- Already set single user mode password protection...", "SKIPPING")
        else:
            for service_file, exec_line in service_items:
                if os.path.exists(service_file):
                    if not os.path.exists(service_file + '_bak'):
                        shutil.copy2(service_file, service_file + '_bak')
                    add_bak_file(service_file + '_bak')
                    with open(service_file, 'r') as read_file:
                        lines = read_file.readlines()
                    is_exist = 0
                    for line in lines:
                        if (not re.match(r'\s*#|$', line)) and re.match(r'\s*ExecStart', line):
                            is_exist = 1
                    if is_exist == 0:
                        with open(service_file, 'a') as add_file:
                            add_file.write(exec_line + '\n')
                    else:
                        with open(service_file, 'w') as write_file:
                            for line in lines:
                                if (not re.match(r'\s*#|$', line)) and re.match(r'\s*ExecStart', line):
                                    write_file.write(exec_line + '\n')
                                else:
                                    write_file.write(line)
            ret, res = subprocess.getstatusoutput('systemctl daemon-reload')
            if ret != 0:
                logger.warning(f"systemctl daemon-reload failed: {res}")
            check_ok = True
            for service_file, exec_line in service_items:
                if not os.path.exists(service_file):
                    check_ok = False
                else:
                    item_ok = False
                    with open(service_file, 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.match(r'\s*ExecStart', line) and '/systemd-sulogin-shell' in line:
                                item_ok = True
                    if not item_ok:
                        check_ok = False
            if check_ok:
                logger.info("set single user mode password protection successfully")
                Display("- Set single user mode password protection...", "FINISHED")
            else:
                logger.warning("set single user mode password protection failed")
                Display("- Set single user mode password protection...", "FAILED")
    else:
        Display("- Skip set single user mode password protection...", "SKIPPING")

