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

#from secScanner.lib import Const

# Program information
PROGRAM_version = "0.1.0"
PROGRAM_releasetype = "v0.1.0"
PROGRAM_NAME = "secScanner"
PROGRAM_name = PROGRAM_NAME
PROGRAM_releasedate = "2023-6-29"
PROGRAM_author = "Yuan Peng"
PROGRAM_author_contact = "pengyuan_yewu@cmss.chinamobile.com"
PROGRAM_website = "https://gitee.com/openeuler/secscanner"
PROGRAM_copyright = "Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved."
# Release version (beta or final)
#alias vi='vim'
PROGRAM_SOURCE="https://gitee.com/openeuler/secscanner"

# Version number of report files (when format changes in future)
REPORT_version_major = "0.1"; REPORT_version_minor = "0"
REPORT_version = f"{REPORT_version_major}.{REPORT_version_minor}"


# Script Info
VER_ID = "SecurityHarden, by pengyuan, 2023-6-29"

if not os.path.exists("/var/log/secScanner"):
    os.makedirs("/var/log/secScanner")

LOGDIR = "/var/log/secScanner/"
LOGFILE = os.path.join(LOGDIR, "secscanner.log")

TMP_DIR=""
RESULT_FILE = os.path.join(LOGDIR, "check_result.relt")

PLANTFORM = ""
MachineType = "" #virtual or physical

scan_HPPOINTS = 0
scan_HPTOTAL = 0


OS_ID = ""
OS_DISTRO = ""
OS_VERSION = ""

BAK_LIST = []

AUTO_ADV_FIX = 0

FIX_SPECIFY_ITEMS = 0 #Flag Value, 1: just fix the specify items. 0: do nothing
FIX_ITEMS = ""   #if user want to fix the specify items

AUTO_BASIC_RESTORE = 0 #auto basic restore
AUTO_ADV_RESTORE = 0   #auto advance restore

UPDATE_INFO = 0  #if user want to see the update info.
UPDATE_CHANGELOG = 0

TEST_PAUSE_TIME = 0
TOTAL_WARNINGS = 0
PIDFILE = ""
TEMP_FILES=""
UNUSED_USER_VALUE = "adm lp sync shutdown halt news uucp operator games nobody rpm smmsp nfsnobody"
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def auto_param():
    global AUTO_ADV_FIX
    global FIX_ITEMS
    global AUTO_BASIC_RESTORE
    global AUTO_ADV_RESTORE

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
