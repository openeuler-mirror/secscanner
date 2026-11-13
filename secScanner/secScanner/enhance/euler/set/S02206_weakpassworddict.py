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
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S02206_weakpassworddict():
    '''
    Function: ensure that the weak password dictionary is set correctly
    '''
    InsertSection("set that the weak password dictionary is set correctly...")
    set_flag = seconf.get('euler', 'set_weakpassworddict')
    if set_flag == 'yes':
        config_files = ['/etc/pam.d/system-auth', '/etc/pam.d/password-auth']
        pwquality_conf = '/etc/security/pwquality.conf'
        already_set = True
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match('password', line) and re.search('pam_pwquality.so', line) \
                                and re.search('dictcheck=0', line):
                            already_set = False
        if os.path.exists(pwquality_conf):
            with open(pwquality_conf, 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match(r'\s*dictcheck\s*=\s*0', line):
                        already_set = False
        if not os.path.exists('/usr/share/cracklib/pw_dict.hwm'):
            already_set = False
        if already_set:
            logger.info("weak password dictionary is already set correctly")
            Display("- Already set the weak password dictionary correctly...", "SKIPPING")
        else:
            for config_file in config_files:
                if os.path.exists(config_file):
                    if not os.path.exists(config_file + '_bak'):
                        shutil.copy2(config_file, config_file + '_bak')
                    add_bak_file(config_file + '_bak')
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                    new_lines = []
                    for line in lines:
                        if re.match('password', line) and re.search('pam_pwquality.so', line) \
                                and re.search('dictcheck=0', line):
                            new_line = ' '.join([field for field in line.split() if field != 'dictcheck=0'])
                            if not new_line.startswith('password'):
                                new_line = 'password ' + new_line
                            new_lines.append(new_line + '\n')
                        else:
                            new_lines.append(line)
                    with open(config_file, 'w') as write_file:
                        write_file.writelines(new_lines)
            if os.path.exists(pwquality_conf):
                if not os.path.exists(pwquality_conf + '_bak'):
                    shutil.copy2(pwquality_conf, pwquality_conf + '_bak')
                add_bak_file(pwquality_conf + '_bak')
                with open(pwquality_conf, 'r') as read_file:
                    lines = read_file.readlines()
                with open(pwquality_conf, 'w') as write_file:
                    for line in lines:
                        if re.match(r'\s*dictcheck\s*=\s*0', line):
                            write_file.write('dictcheck = 1\n')
                        else:
                            write_file.write(line)
            if os.path.exists('/usr/share/cracklib/pw_dict.hwm'):
                ret, res = subprocess.getstatusoutput(
                    'cracklib-unpacker /usr/share/cracklib/pw_dict > /var/tmp/dictionary.txt')
                if ret == 0 and os.path.exists('/var/tmp/dictionary.txt') and os.path.getsize('/var/tmp/dictionary.txt') > 0:
                    ret2, res2 = subprocess.getstatusoutput('create-cracklib-dict /var/tmp/dictionary.txt')
                    if ret2 == 0:
                        logger.info("update the weak password dictionary successfully")
                        os.remove('/var/tmp/dictionary.txt')
                    else:
                        logger.warning(f"update the weak password dictionary failed: {res2}")
                else:
                    logger.warning(f"unpack the weak password dictionary failed: {res}")
            check_ok = True
            for config_file in config_files:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if re.match('password', line) and re.search('pam_pwquality.so', line) \
                                    and re.search('dictcheck=0', line):
                                check_ok = False
            if os.path.exists(pwquality_conf):
                with open(pwquality_conf, 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if re.match(r'\s*dictcheck\s*=\s*0', line):
                            check_ok = False
            if not os.path.exists('/usr/share/cracklib/pw_dict.hwm'):
                check_ok = False
            if check_ok:
                logger.info("set the weak password dictionary successfully")
                Display("- Set the weak password dictionary correctly...", "FINISHED")
            else:
                logger.warning("set the weak password dictionary failed")
                Display("- Set the weak password dictionary correctly...", "FAILED")
    else:
        Display("- Skip set the weak password dictionary...", "SKIPPING")

