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
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")

def C0364_sysrq():
    InsertSection("Check set of kernel.sysrq in sysctl config file")
    config_file = "/etc/sysctl.conf"
    if os.path.exists(config_file):
        flag = False
        with open("/etc/sysctl.conf", "r") as read_file:
            lines = read_file.readlines()
            sysrq_count = 0  # 计数器用于追踪配置出现次数
            for line in lines:
                if re.match(r"kernel\.sysrq\s*=\s*[01]", line):  # 匹配所有 kernel.sysrq 配置
                    sysrq_count += 1
                    if re.match(r"kernel\.sysrq\s*=\s*0", line):
                        flag = True
            # 如果存在多条配置或值不为0，将flag设为False
            if sysrq_count > 1 or not flag:
                flag = False
        if flag:
            logger.info("Check set of kernel.sysrq in sysctl config file")
            Display("- Check set of kernel.sysrq in sysctl config file", "OK")
        else:
            with open(RESULT_FILE, 'a') as file:
                file.write("\nC0364\n")
            logger.warning("WRN_C0364: %s", WRN_C0364)
            logger.warning("SUG_C0364: %s", SUG_C0364)
            Display("- Wrong set of kernel.sysrq in sysctl config file...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC0364\n")
        logger.warning(f"WRN_C0364: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C0364: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
