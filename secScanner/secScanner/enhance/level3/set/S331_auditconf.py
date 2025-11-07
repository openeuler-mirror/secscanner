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
from secScanner.lib import *
from secScanner.gconfig import *
import logging
logger = logging.getLogger("secscanner")

'''
auditd_conf="/etc/audit/auditd.conf"
# 使用grep命令获取max_log_file_action和admin_space_left_action的配置行，并移除空格
max_log_file_action_line=$(grep '^\s*max_log_file_action\s*=' "$auditd_conf")
admin_space_left_action_line=$(grep '^\s*admin_space_left_action\s*='
"$auditd_conf")
space_left_action_line=$(grep '^\s*space_left_action\s*=' "$auditd_conf")
# 检查是否找到max_log_file_action的配置行
if [ -n "$max_log_file_action_line" ]; then
# 使用sed命令将等号后的值修改为keep_logs
sudo sed -i 's/^\(\s*max_log_file_action\s*=\s*\).*/\1keep_logs/'
"$auditd_conf"
# 检查sed命令是否成功执行
if [ $? -eq 0 ]; then
echo "3.3.1 repaired max_log_file_action 已成功设置为 keep_logs"
else
echo "设置 max_log_file_action 为 keep_logs 失败"
fi
else
echo "未找到 max_log_file_action 行"
fi

'''
def S331_auditconf():
    InsertSection("Set audit config...")
    SET_AUDITCONF = seconf.get('level3', 'set_auditconf')
    config_file = "/etc/audit/auditd.conf"
    if SET_AUDITCONF == 'yes':
        if os.path.exists(config_file):
            if not os.path.exists('/etc/audit/auditd.conf_bak'):
                shutil.copy2('/etc/audit/auditd.conf', '/etc/audit/auditd.conf_bak')
            add_bak_file('/etc/audit/auditd.conf_bak')
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^max_log_file_action', line):
                        if re.search(r'^max_log_file_action = keep_logs', line):
                            logger.info("audit.conf is already set")
                            Display("- max_log_file_action in audit.conf already set correctly...", "FINISHED")
                            return
            WRITE_FLAG = False
            with open(config_file, 'w') as write_file:
                for line in lines:
                    if re.search(r'^max_log_file_action', line):
                        write_file.write("max_log_file_action = keep_logs\n")
                        WRITE_FLAG = True
                    else:
                        write_file.write(line)
            if WRITE_FLAG == False:
                with open(config_file, 'a') as add_file:
                    add_file.write("\nmax_log_file_action = keep_logs\n")
            FLAG = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search(r'^max_log_file_action = keep_logs', line):
                        logger.info("max_log_file_action in audit.conf is set")
                        FLAG = True
            if FLAG == False:
                logger.error("max_log_file_action in audit.conf set incorrectly")
                Display("- max_log_file_action in audit.conf set incorrectly...", "FAILED")
            else:
                logger.info("max_log_file_action in audit.conf set correctly")
                Display("- max_log_file_action in audit.conf set correctly...", "FINISHED")
        else:
            logger.error("Config file not found, auditconf set incorrectly")
            Display("- Config file not found, auditconf set failed...", "FAILED")
    else:
        Display("- Skip set max_log_file_action in audit.conf due to config file...", "SKIPPING")


