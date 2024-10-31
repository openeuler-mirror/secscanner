import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")

#1.(3)1应能对事件生成审计日志。=================================
# 定义要检查的审计规则
audit_rules = [
    ('chown', 'fchown', 'fchownat'),
    ('chmod', 'fchmod', 'fchmodat'),
    ('creat', 'open', 'openat', 'open_by_handle_at'),
    ('mkdir', 'mknod'),
    ('unlink', 'unlinkat', 'rename', 'renameat'),
    ('execve'),
]

# 定义规则文件的路径
audit_rules_file = '/etc/audit/rules.d/audit.rules'
audit_rules_file_bak = '/etc/audit/rules.d/audit.rules_bak'
generate_audit_log = seconf.get('group', 'generate_audit_log')

# 定义一个函数来检查规则是否存在
def rule_exists(rule_list, rule_string):
    pattern = re.escape(rule_string)
    for rule in rule_list:
        #pattern = rf'exit,always.*-F.*arch=b64.*-S.*{rule}'
        if re.search(pattern, rule, re.MULTILINE):
            return True
    return False

# 定义一个函数来添加规则
def add_rule( new_rule):
    with open(audit_rules_file, 'a') as file:
        file.write(f'\n{new_rule}\n')

def set_audit_log():
    num = 0
    num_ex = 0
    if generate_audit_log == 'yes':
        if os.path.exists(audit_rules_file):
            if not os.path.exists(audit_rules_file_bak):
                shutil.copy2(audit_rules_file, audit_rules_file_bak)

            for rule_group in audit_rules:
            # 读取现有的审计规则
                with open(audit_rules_file, 'r') as file:
                    rules_content = file.read()

                if not rule_group == 'execve':
                    rules_add = ' -S '.join(rule_group)
                    rule_to_check = rule_group[0] if rule_group[0] != 'unlink' else 'delete'
                    if not rule_exists(rules_content.split('\n'), rule_group[0]):
                        new_rule = f'-a exit,always -F arch=b64 -S {rules_add} -F auid>=1000 -F auid!=4294967295 -k {rule_to_check}'
                        add_rule(new_rule)
                        num += 1
                else:
                    if not rule_exists(rules_content.split('\n'), rule_group):
                        new_rule = f'-a exit,always -F arch=b64 -S execve -F auid=0 -F key=op_root_cmd'
                        add_rule(new_rule)
                        num_ex += 1
            if num == 5 and num_ex == 1:
                logger.info("Set generate audit log. checking ok")
                Display("- Set generate audit log ...", "FINISHED")
            elif num == 0 and num_ex == 0:
                logger.info("No relevant configuration available")
                Display("- Set generate audit log ...", "FAILED")
            else:
                logger.info("Incomplete or incorrect configuration")
                Display("- Set generate audit log ...", "FAILED")
        else:
            logger.info(f"file {audit_rules_file} not exists ")
            Display(f"- file {audit_rules_file}  not exists...", "FAILED")
    else:
         Display("- Skip generate audit log due to config file...", "SKIPPING")


def S03_genAuditlog():
    OS_ID = get_value("OS_ID")
    OS_DISTRO = get_value("OS_DISTRO")
    InsertSection("set generate audit log")
    if OS_ID.lower() == 'bclinux' and OS_DISTRO == '7':
        set_audit_log()
    else:
        logger.info(f"we do not support {OS_ID}-{OS_DISTRO} at this moment")
        Display(f"- We do not support {OS_ID}-{OS_DISTRO} at this moment...", "WARNING")



