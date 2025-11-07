#!/opt/secScanner/virtualenv/bin/python3
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


import re
import os
import getpass
import subprocess

# 检查密码复杂度的函数
def check_password_complexity(password):
    # 密码复杂度要求
    # 1. 密码长度不小于8位
    # 2. 至少包含三种字符（大小写字母、特殊符号、数字）
    if len(password) < 8:
        return 0

    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    if has_lower and has_upper and has_digit and has_special:
        return 1
    else:
        return 0

def change_permissions(path, mode):
    os.chmod(path, mode)

def add_user_to_wheel_group(userlist):
    # Define the wheel group line format
    wheel_group_line = "wheel:x:10:{}\n".format(user_list)

    # Read the /etc/group file
    with open("/etc/group", "r") as group_file:
        group_lines = group_file.readlines()

    # Check if the wheel group already exists
    wheel_group_exists = False
    for i, line in enumerate(group_lines):
        if line.startswith("wheel:"):
            wheel_group_exists = True
            group_lines[i] = wheel_group_line  # Replace the existing line
            break

    # If the wheel group doesn't exist, append it to the end
    if not wheel_group_exists:
        group_lines.append(wheel_group_line)

    # Write back the modified /etc/group file
    with open("/etc/group", "w") as group_file:
        group_file.writelines(group_lines)

if __name__ == '__main__':

    users = ["系统管理员", "审计管理员", "安全管理员"]
    user_list = "root"


    print("根据《信息安全技术网络安全等级保护基本要求（GB/T 22239-2019）》应授予管理用户所需的最小权限,")
    print("实现管理用户的权限分离: 用户需要至少创建系统管理员、审计管理员和安全管理员三个用户")

    for user in users:
        while True:
            name = input(f"请输入要创建的{user}用户：")
            try:
                # 创建用户
                subprocess.check_call(["useradd", name])
                break
            except subprocess.CalledProcessError:
                print(f"无效的{user}用户名, 无法执行useradd命令")

        passwd = ""
        re_passwd = ""
        status = 0

        while status != 1:
            passwd = getpass.getpass(f"请输入{users}用户的密码:\n"
                                     f"根据《信息安全技术网络安全等级保护基本要求（GB/T 22239-2019）》密码复杂度要求：\n"
                                     f"\t1.密码长度不小于8位，\n"
                                     f"\t2.至少包含三种字符（大小写字母、特殊符号、数字）")
            status = check_password_complexity(passwd)

            if status == 0:
                print("您的密码复杂度太低,请重新输入:")
            else:
                while passwd != re_passwd:
                    re_passwd = getpass.getpass(f"请再次确认您的密码:")
                    if passwd != re_passwd:
                        print("您两次输入的密码不一致，请您重新输入:")
                        re_passwd = ""
                        status = 0
                    else:
                        status = 1

        # 更新用户密码
        # 使用 communicate 方法来提供输入
        with subprocess.Popen(["chpasswd"], stdin=subprocess.PIPE, universal_newlines=True) as proc:
            proc.communicate(f"{name}:{passwd}\n")

        user_list += "," + name

    user_list = user_list.split(",", 1)[1]

    print("用户创建完成")

    # Change permissions of /home/* directories to 750
    for directory in os.listdir("/home"):
        full_path = os.path.join("/home", directory)
        if os.path.isdir(full_path):
            change_permissions(full_path, 0o750)

    # Add each user to the wheel group and grant su privileges
    # Output a message regarding su privileges
    print("根据《信息安全技术网络安全等级保护基本要求（GB/T 22239-2019）》")
    print("加固建议: 该普通用户、审计员和安全员获得执行su命令的权限")

    add_user_to_wheel_group(user_list)

