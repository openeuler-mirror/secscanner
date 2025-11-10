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
# 检查是否找到admin_space_left_action的配置行
if [ -n "$admin_space_left_action_line" ]; then
# 使用sed命令将等号后的值修改为halt
sudo sed -i 's/^\(\s*admin_space_left_action\s*=\s*\).*/\1halt/'
"$auditd_conf"
# 检查sed命令是否成功执行
if [ $? -eq 0 ]; then
echo "3.3.2 repaired admin_space_left_action 已成功设置为 halt"
else
echo "3.3.2 repaired 设置 admin_space_left_action 为 halt 失败"
fi
else
echo "未找到 admin_space_left_action 行"
fi
# 检查是否找到admin_space_left_action的配置行
if [ -n "$space_left_action_line" ]; then
# 使用sed命令将等号后的值修改为email
sudo sed -i 's/^\(\s*space_left_action\s*=\s*\).*/\1email/' "$auditd_conf"
# 检查sed命令是否成功执行
if [ $? -eq 0 ]; then
echo "3.3.2 repaired space_left_action 已成功设置为 emaill"
else
echo "设置 space_left_action 为 email 失败"
fi
else
echo "未找到 space_left_action 行"
加固脚本执行结果如下图所示，加固后的项目会输出repaired.
fi

'''
def S332_auditconf2():
    InsertSection("Set audit config...")
    SET_AUDITCONF = seconf.get('level3', 'set_auditconf2')
    config_file = "/etc/audit/auditd.conf"
    if SET_AUDITCONF == 'yes':
        if os.path.exists(config_file):
            if not os.path.exists('/etc/audit/auditd.conf_bak'):
                shutil.copy2('/etc/audit/auditd.conf', '/etc/audit/auditd.conf_bak')
            add_bak_file('/etc/audit/auditd.conf_bak')
            admin_action_set = False
            action_set = False
            with open(config_file, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.search('space_left_action', line):
                        if re.match('space_left_action = email', line):
                            logger.info("space_left_action is already set")
                            action_set = True
                        if re.match('admin_space_left_action = halt', line):
                            logger.info("admin_space_left_action is already set")
                            admin_action_set = True
            if action_set == True and admin_action_set == True:
                logger.info("space_left_action and admin_space_left_action are already set")
                Display("- space_left_action and admin_space_left_action are already set...", "FINISHED")
            else:
                WRITE_FLAG = False
                WRITE_FLAG_admin = False
                with open(config_file, 'w') as write_file:
                    for line in lines:
                        if re.match('space_left_action', line):
                            write_file.write("space_left_action = email\n")
                            WRITE_FLAG = True
                        elif re.match('admin_space_left_action', line):
                            write_file.write("admin_space_left_action = halt\n")
                            WRITE_FLAG_admin = True
                        else:
                            write_file.write(line)
                if WRITE_FLAG == False:
                    with open(config_file, 'a') as add_file:
                        add_file.write("\nspace_left_action = email\n")
                if WRITE_FLAG_admin == False:
                    with open(config_file, 'a') as add_file:
                        add_file.write("\nadmin_space_left_action = halt\n")
                FLAG = False
                FLAG_admin = False
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match('admin_space_left_action = halt', line):
                            logger.info("admin_space_left_action in audit.conf is set")
                            FLAG_admin = True
                        if re.match('space_left_action = email', line):
                            logger.info("space_left_action in audit.conf is set")
                            FLAG = True
                if FLAG == True and FLAG_admin == True:
                    logger.info("admin_space_left_action and space_left_action in audit.conf set correctly")
                    Display("- admin_space_left_action and space_left_action in audit.conf set correctly...", "FINISHED")
                else:
                    logger.error("admin_space_left_action and space_left_action in audit.conf set incorrectly")
                    Display("- admin_space_left_action and space_left_action in audit.conf set incorrectly...", "FAILED")
        else:
            logger.error("Config file not found, auditconf set incorrectly")
            Display("- Config file not found, auditconf set failed...", "FAILED")
    else:
        Display("- Skip set admin_space_left_action and space_left_action in audit.conf due to config file...", "SKIPPING")


