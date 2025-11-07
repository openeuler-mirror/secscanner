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
import sys
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")

def S31_anonymousFTP():
    set_ftp_anonymous = seconf.get('advance', 'set_ftp_anonymous')
    InsertSection("Set the prohibit anonymous FTP...")
    if set_ftp_anonymous == 'yes':
        if os.path.exists('/etc/vsftpd/vsftpd.conf') and not os.path.exists('/etc/vsftpd/vsftpd.conf_bak'):
            shutil.copy2('/etc/vsftpd/vsftpd.conf', '/etc/vsftpd/vsftpd.conf_bak')
        add_bak_file('/etc/vsftpd/vsftpd.conf_bak')
            # -----------------set the restrictFTPdir----------------
        if os.path.exists('/etc/vsftpd/vsftpd.conf'):
            with open('/etc/vsftpd/vsftpd.conf', 'r+') as f:
                lines = f.readlines()
                anonymous_exists = False
                for i, line in enumerate(lines):
                    if line.strip().startswith("#anonymous_enable"):
                        anonymous_exists = True
                        lines[i] = lines[i].replace("#", "")
                        if not re.search('NO', line):
                            lines[i] = "anonymous_enable=NO\n"
                        break
                    elif line.strip().startswith("anonymous_enable"):
                        anonymous_exists = True
                        if not re.search('NO', line):
                            lines[i] = "anonymous_enable=NO\n"
                        break
                if not anonymous_exists:
                    lines.append("anonymous_enable=NO\n")
                f.seek(0)
                f.writelines(lines)
                f.truncate()

            CHECK_EXIST = 0
            with open('/etc/vsftpd/vsftpd.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('anonymous_enable', line):
                        IS_EXIST = 1
                        temp = line.strip('\n').split('=')
                        if temp[0] == 'anonymous_enable' and temp[1] == 'NO':
                            CHECK_EXIST = 1

            if not anonymous_exists:
                logger.info("set the prohibit anonymous FTP failed, no set option")
                Display("- Set the prohibit anonymous FTP...", "FAILED")
            elif CHECK_EXIST == 0:
                logger.info("set the prohibit anonymous FTP failed, wrong setting")
                Display("- Set the prohibit anonymous FTP...", "FAILED")
            else:
                ret, result = subprocess.getstatusoutput('systemctl is-active vsftpd')
                if ret != 0:
                    flag, out = subprocess.getstatusoutput('systemctl start vsftpd')
                    if flag != 0:
                        logger.warning('Start vsftpd failed')
                        Display("- Start vsftpd service failed...", "FAILED")
                        return
                else:
                    flag, out = subprocess.getstatusoutput('systemctl restart vsftpd')
                    if flag != 0:
                        logger.warning('Restart vsftpd failed')
                        Display("- Restart vsftpd service failed...", "FAILED")
                        return

                logger.info("set the prohibit anonymous FTP successfully")
                Display("- Set the prohibit anonymous FTP...", "FINISHED")
        else:
            Display("- filepath /etc/vsftpd/vsftpd.conf not exist...", "SKIPPING")
    else:
        Display("- Skip set prohibit anonymous FTP due to config file...", "SKIPPING")
