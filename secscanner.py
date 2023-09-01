#!/usr/bin/python3
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
import platform

from secScanner.gconfig import *
g_init()
from secScanner.commands.basic import *

def check_python_version():
    python_version = platform.python_version().split('.')[0]
    if python_version == "3":
        return
    else:
        print('Invalid python version requested: %s' % python_version)

if __name__ == "__main__":
    check_python_version()

    logger = logging.getLogger("secscanner")
    seconf.LOGFILE = seconf.get('main', 'LOGFILE')
    seconf.LOG_LEVEL = seconf.get('main', 'LOG_LEVEL')
    
    if 'debug' == seconf.LOG_LEVEL:
        logger.setLevel(logging.DEBUG)
    elif 'error' == seconf.LOG_LEVEL:
        logger.setLevel(logging.ERROR)
    elif 'info' == seconf.LOG_LEVEL:
        logger.setLevel(logging.INFO)
    elif 'warn' == seconf.LOG_LEVEL:
        logger.setLevel(logging.WARN)
    else:
        # set ERROR as default logger level
        logger.setLevel(logging.ERROR)

    logging.basicConfig(filename = seconf.LOGFILE,
            filemode = 'w',
            format = '[%(asctime)s] [%(levelname)s] [%(name)s] >>>  %(message)s',
            datefmt = '%Y-%m-%d %H:%M')
    scan_command()
