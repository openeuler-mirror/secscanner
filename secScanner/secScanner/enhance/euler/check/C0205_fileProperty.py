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
import re
from secScanner.lib import *
from secScanner.gconfig import *

logger = logging.getLogger("secscanner")


def C0205_fileProperty():
    InsertSection("check file property set")
    BASIC_OPTIONS = seconf.options('euler')  # search basic and show all options
    CHMOD_644_FILE = []
    CHMOD_000_FILE = []

    if 'chmod_644_file' in BASIC_OPTIONS:  # if there is a 'chmod 644 file', save the value in a list
        CHMOD_644_FILE = seconf.get('euler', 'chmod_644_file').split()
    if 'chmod_000_file' in BASIC_OPTIONS:
        CHMOD_000_FILE = seconf.get('euler', 'chmod_000_file').split()

    tmp_count = 1  # count the number of WARN_C0205_tmp_count
    for i in CHMOD_644_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
            if file_permission == '644':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0205\n")
                warn_str = "WRN_C0205_" + str(tmp_count)
                sugs_str = "SUG_C0205_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1

    for i in CHMOD_000_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]
            if file_permission == '000':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC0205\n")
                warn_str = "WRN_C0205_" + str(tmp_count)
                sugs_str = "SUG_C0205_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1


