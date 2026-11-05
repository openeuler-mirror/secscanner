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
import secrets
import shutil
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02209_grubpassword():
    '''
    Function: ensure that grub is protected with a password, generate a random password and write it into /root/grubpassword.txt
    '''
    InsertSection("set grub password protection...")
    set_flag = seconf.get('euler', 'set_grubpassword')
    if set_flag == 'yes':
        grub_dirs = []
        if os.path.isdir('/boot/efi/EFI/openEuler'):
            grub_dirs.append('/boot/efi/EFI/openEuler')
        if os.path.isdir('/boot/grub2'):
            grub_dirs.append('/boot/grub2')
        if not grub_dirs:
            logger.warning("grub config directory does not exist")
            Display("- Grub config directory not found...", "FAILED")
        else:
            need_set = False
            for grub_dir in grub_dirs:
                user_cfg = os.path.join(grub_dir, 'user.cfg')
                if not os.path.exists(user_cfg):
                    need_set = True
                else:
                    with open(user_cfg, 'r') as read_file:
                        lines = read_file.readlines()
                        if not any(re.search(r'GRUB2_PASSWORD=grub\.pbkdf2\.sha512\.\d+\.', line) for line in lines):
                            need_set = True
            if not need_set:
                logger.info("grub password is already set in user.cfg")
                Display("- Already set grub password protection...", "SKIPPING")
            else:
                password = secrets.token_urlsafe(16)
                ret = -1
                hash_value = ''
                try:
                    result = subprocess.run(['grub2-mkpasswd-pbkdf2'],
                                            input=password + '\n' + password + '\n',
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    ret = result.returncode
                    output = result.stdout.decode('utf-8', errors='ignore') + result.stderr.decode('utf-8', errors='ignore')
                    match = re.search(r'grub\.pbkdf2\.sha512\.\d+\.\S+', output)
                    if match:
                        hash_value = match.group(0).strip()
                except (OSError, ValueError):
                    ret = -1
                if ret != 0 or not hash_value:
                    logger.warning("generate the grub password hash failed")
                    Display("- Generate the grub password hash...", "FAILED")
                else:
                    if not os.path.exists('/root/grubpassword.txt'):
                        with open('/root/grubpassword.txt', 'w') as write_file:
                            write_file.write(password + '\n')
                        os.chmod('/root/grubpassword.txt', 0o600)
                    for grub_dir in grub_dirs:
                        user_cfg = os.path.join(grub_dir, 'user.cfg')
                        if os.path.exists(user_cfg):
                            if not os.path.exists(user_cfg + '_bak'):
                                shutil.copy2(user_cfg, user_cfg + '_bak')
                            add_bak_file(user_cfg + '_bak')
                            with open(user_cfg, 'r') as read_file:
                                lines = read_file.readlines()
                        else:
                            lines = []
                        with open(user_cfg, 'w') as write_file:
                            replaced = False
                            for line in lines:
                                if re.match(r'\s*GRUB2_PASSWORD=', line):
                                    write_file.write(f'GRUB2_PASSWORD={hash_value}\n')
                                    replaced = True
                                else:
                                    write_file.write(line)
                            if not replaced:
                                write_file.write(f'GRUB2_PASSWORD={hash_value}\n')
                        grub_cfg = os.path.join(grub_dir, 'grub.cfg')
                        if os.path.exists(grub_cfg):
                            if not os.path.exists(grub_cfg + '_bak'):
                                shutil.copy2(grub_cfg, grub_cfg + '_bak')
                            add_bak_file(grub_cfg + '_bak')
                            with open(grub_cfg, 'r') as read_file:
                                grub_lines = read_file.readlines()
                            has_pbkdf2 = False
                            for line in grub_lines:
                                if 'password_pbkdf2' in line or 'grub.pbkdf2.sha512' in line:
                                    has_pbkdf2 = True
                            if not has_pbkdf2:
                                grub_lines.insert(0, 'password_pbkdf2 root ${GRUB2_PASSWORD}\n')
                                with open(grub_cfg, 'w') as write_file:
                                    write_file.writelines(grub_lines)
                    check_ok = True
                    for grub_dir in grub_dirs:
                        user_cfg = os.path.join(grub_dir, 'user.cfg')
                        if not os.path.exists(user_cfg):
                            check_ok = False
                        else:
                            with open(user_cfg, 'r') as read_file:
                                lines = read_file.readlines()
                                if not any(re.search(r'GRUB2_PASSWORD=grub\.pbkdf2\.sha512\.\d+\.', line) for line in lines):
                                    check_ok = False
                    if check_ok:
                        logger.info("set grub password protection successfully, the password is saved in /root/grubpassword.txt")
                        Display("- Set grub password protection, the password is saved in /root/grubpassword.txt...", "FINISHED")
                    else:
                        logger.warning("set grub password protection failed")
                        Display("- Set grub password protection...", "FAILED")
    else:
        Display("- Skip set grub password protection...", "SKIPPING")

