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
from pathlib import Path
import configparser

'''
The following functions is a dict to save global values
'''
def g_init():  # initiation
    global _global_dict
    _global_dict = {}

def set_value(key, value):
    # this function can save key/value in global dict
    # u can use this function after import
    _global_dict[key] = value

def get_value(key):
    # this function can use key to get value in global dict
    # u can use this function after import
    try:
        return _global_dict[key]
    except:
        print('there is no ' + key + ' in global dict\r\n')

def show_dict():
    # when u need to check if there is a key in global dict or something else
    # this function will return global dict
    # use :  if "key" in show_dict():
    return _global_dict
'''
The above functions is a dict to save global values
'''
# Program information
PROGRAM_VERSION = "0.1.0"
PROGRAM_RELEASE = "v0.1.0"
PROGRAM_NAME = "secScanner"
PROGRAM_UPDATEDATE = "2023-6-29"
PROGRAM_AUTHOR = "Yuan Peng"
PROGRAM_CONTACTEMAIL = "pengyuan_yewu@cmss.chinamobile.com"
PROGRAM_WEBSITE = "https://gitee.com/openeuler/secscanner"
PROGRAM_COPYRIGHT = "Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved."

# Script Info
VER_ID = "SecurityHarden, by pengyuan, 2023-6-29"

if not os.path.exists("/var/log/secScanner"):
    os.makedirs("/var/log/secScanner")

LOGDIR = "/var/log/secScanner/"
LOGFILE = os.path.join(LOGDIR, "secscanner.log")

RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

#
#################################################################################
#
# * Colors
#
# For improved display
#
#################################################################################
#
WARNING = "\033[1;31m"          # Bad (red)
SECTION = "\033[1;33m"          # Section (yellow)
NOTICE = "\033[1;33m"           # Notice (yellow)
OK = "\033[1;32m"               # Ok (green)
BAD = "\033[1;31m"              # Bad (red)

# Normal color names
YELLOW_BLINK = "\033[1;5;33m"
MAGENTA = "\033[1;35m"

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
ORANGE = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"

NORMAL = "\033[0;39m"


global seconf
def load_config(configfile):
    config = configparser.ConfigParser()
    # read default config from default ditct
    #config.read_dict(default_values)
    if not os.path.exists(configfile):
        print("%s config file not found!" % configfile)
        exit(1)
    # reload config from configfile
    config.read(configfile)

    return config

seconf = load_config("/etc/secScanner/secscanner.cfg")
