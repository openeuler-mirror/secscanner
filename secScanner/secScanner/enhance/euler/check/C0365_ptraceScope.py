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

def C0365_ptraceScope():
    InsertSection("Check set of kernel.yama.ptrace_scope in sysctl config file")      
    
    config_file = "/etc/sysctl.conf"
    if os.path.exists(config_file):
        ret, res = subprocess.getstatusoutput('grep "^kernel.yama.ptrace_scope" /etc/sysctl.conf')     
        if ret == 0:
            ptrace_scope_list = res.split('\n')
            flag = False  
            for ptrace_scope_value in ptrace_scope_list:         
                if re.match("kernel.yama.ptrace_scope=2", ptrace_scope_value):
                    flag = True
            
            if flag:
                logger.info("Check set of kernel.yama.ptrace_scope in sysctl config file")
                Display("- Check set of kernel.yama.ptrace_scope in sysctl config file", "OK")
            else:
                with open(RESULT_FILE, 'a+') as file:
                    file.write("\nC0365\n")
                logger.warning("WRN_C0365: %s", WRN_C0365)
                logger.warning("SUG_C0365: %s", SUG_C0365)
                Display("- Wrong set of kernel.yama.ptrace_scope in sysctl config file...", "WARNING")
        else:
            logger.warning("Not set of kernel.yama.ptrace_scope in sysctl config file")
            Display("- Not set of kernel.yama.ptrace_scope in sysctl config file...", "WARNING")
    else:
        with open(RESULT_FILE, 'a+') as file:
            file.write("\nC0365\n")
        logger.warning(f"WRN_C0365: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0365: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
    
    config_d = "/etc/sysctl.d"
    if os.path.exists(config_d):
        ret1, res1 = subprocess.getstatusoutput('grep "^kernel.yama.ptrace_scope" /etc/sysctl.d/*')
        if ret1 == 0:
            ptrace_scope_list = res1.split('\n')
            flag = False           
            for ptrace_scope_value in ptrace_scope_list:           
                if re.match("kernel.yama.ptrace_scope=2", ptrace_scope_value):
                    flag = True
            
            if flag:
                logger.info("Check set of kernel.yama.ptrace_scope in sysctl.d/*")
                Display("- Check set of kernel.yama.ptrace_scope in sysctl.d/*", "OK")
            else:
                with open(RESULT_FILE, 'a+') as file:
                    file.write("\nC0365\n")
                logger.warning("WRN_C0365: %s", WRN_C0365)
                logger.warning("SUG_C0365: %s", SUG_C0365)
                Display("- Wrong set of kernel.yama.ptrace_scope in sysctl.d/*...", "WARNING")
        else:
            logger.warning("Not set of kernel.yama.ptrace_scope in sysctl.d/* ")
            Display("- Not set of kernel.yama.ptrace_scope in sysctl.d/*...", "WARNING")
    else:
        with open(RESULT_FILE, 'a+') as file:
            file.write("\nC0365\n")
        logger.warning(f"WRN_C0365: {config_d} {WRN_no_file}")
        logger.warning(f"SUG_C0365: {config_d} {SUG_no_file}")
        Display(f"- Config file: {config_d} not found...", "SKIPPING")