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
import os
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0126_LdapServer():
    set_remove_LdapServer = seconf.get('euler', 'set_remove_LdapServer')
    InsertSection("Remove the openldap-servers in your Linux System...")
    if set_remove_LdapServer == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q openldap-servers')
        if ret != 0:
            logger.info(f'The status is:{res}')
            Display("- No package for the openldap-servers...", "SKIPPING")
        else:
            try:
                set_result,_= subprocess.getstatusoutput(' yum remove openldap-servers -y')
            except Exception:
                os.system('dnf remove openldap-servers -y')
                
            if set_result == 0:
                logger.info("Set remove the openldap-servers, checking ok")
                Display("- Set remove the openldap-servers...", "FINISHED")
            else:
                logger.warning("Set remove the openldap-servers failed")
                Display("- Set remove the openldap-servers...", "FAILED")
    else:
        Display("- Skip set remove the openldap-servers...", "SKIPPING")
    