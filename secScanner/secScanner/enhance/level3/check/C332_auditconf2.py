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


'''
# 检查space_left_action、action_mail_acct和admin_space_left_action参数配置
check_audit_conf_params() {
local params=("space_left_action" "action_mail_acct"
"admin_space_left_action")
local expected_values=("email" "root" "halt")
local pass_count=0
for (( i=0; i<${#params[@]}; i++ )); do
local param_name="${params[$i]}"
local expected_value="${expected_values[$i]}"
local param_value=$(grep -q "^\s*$param_name\s*=" "$auditd_conf" && grep
"^\s*$param_name\s*=" "$auditd_conf" | sed
's/^[[:space:]]*'"$param_name"'[[:space:]]*=[[:space:]]*//')
if [[ "$param_value" == "$expected_value" ]]; then
((pass_count++))
fi
done
'''
import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C332_auditconf2():
    InsertSection("check the config of audit.conf part 2")
    config_file = "/etc/audit/auditd.conf"
    if os.path.exists(config_file):
        space_left_action = ''
        action_mail_acct = ''
        admin_space_left_action = ''
        config_file_path = "/etc/audit/auditd.conf"
        with open(config_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not re.match(r'^\s*#', line):
                    if re.match(r'^\s*space_left_action\s*=', line):
                        space_left_action = line.split('=')[1].strip()
                    if re.match(r'^\s*action_mail_acct\s*=', line):
                        action_mail_acct = line.split('=')[1].strip()
                    if re.match(r'^\s*admin_space_left_action\s*=', line):
                        admin_space_left_action = line.split('=')[1].strip()
        if space_left_action == "email" and action_mail_acct == "root" and admin_space_left_action == "halt":
            logger.info("audit.conf set correctly, checking ok")
            Display("- Has set audit.conf correctly ...", "OK")
        else:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC332\n")
            logger.warning("WRN_C332: %s", WRN_C332)
            logger.warning("SUG_C332: %s", SUG_C332)
            Display("- Wrong audit.conf set...", "WARNING")
    else:
        with open(RESULT_FILE, 'a') as file:
            file.write("\nC332\n")
        logger.warning(f"WRN_C332: {config_file} {WRN_no_file}")
        logger.warning(f"SUG_C332: {config_file} {SUG_no_file}")
        Display(f"- Config file: {config_file} not found...", "SKIPPING")
