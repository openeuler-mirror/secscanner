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
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0130_LdapClient():
    InsertSection("Check whether the LdapClient software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q openldap-clients')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0130\n")
        logger.warning("WRN_C0130: %s", WRN_C0130)
        logger.warning("SUG_C0130: %s", SUG_C0130)
        Display(f"- Check the openldap-clients software is installed...", "WARNING")
    else:
        logger.info(f"The openldap-clients status is: {res}")
        Display(f"- Check the openldap-clients software is uninstall...", "OK")