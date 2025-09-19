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
import stat
import re
import sys
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import pathlib
import pwd
import grp
    
logger = logging.getLogger("secscanner")

def chown_root(filepath):
    # 获取root用户和组的ID
    uid = pwd.getpwnam('root').pw_uid
    gid = grp.getgrnam('root').gr_gid

    # 更改文件的所有者和组
    os.chown(filepath, uid, gid)

def S0205_fileProperty():
    InsertSection("Set the file property...")
    SET_FILE_PROPERTY = seconf.get('euler', 'set_file_property')
    BASIC_OPTIONS = seconf.options('euler')  # search basic and show all options
    CHMOD_644_FILE = []
    CHMOD_000_FILE = []
    if 'chmod_644_file' in BASIC_OPTIONS:  # if there is a 'chmod 644 file', save the value in a list
        CHMOD_644_FILE = seconf.get('euler', 'chmod_644_file').split()
    if 'chmod_000_file' in BASIC_OPTIONS:
        CHMOD_000_FILE = seconf.get('euler', 'chmod_000_file').split()
    
    if SET_FILE_PROPERTY == 'yes':
        record_file = '/etc/secscanner.d/fdproperty_record'
        if not os.path.exists(record_file):
            pathlib.Path(record_file).touch()
        if not os.path.getsize(record_file):
            with open(record_file, 'w') as f:
                if CHMOD_644_FILE:
                    for i in CHMOD_644_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_000_FILE:
                    for i in CHMOD_000_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")

        ##chmod file and dir
        if CHMOD_644_FILE:
            for i in CHMOD_644_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o644)
                    chown_root(i)
        if CHMOD_000_FILE:
            for i in CHMOD_000_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o000)
                    chown_root(i)

        logger.info("Set the file property finished")
        Display("- Set the file property...", "FINISHED")
    else:
        Display("- Skip set security file property due to config file...", "SKIPPING")
