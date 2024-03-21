# -*- coding: utf-8 -*-
'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''
import os
import sys
import subprocess
import logging
import re
logger = logging.getLogger('secscanner')

class sec_service:
    def reload(self):
        cmd = 'systemctl daemon-reload'
        ret, result = subprocess.getstatusoutput(cmd)
        if ret !=0:
            logger.error("systemd service reload failed")
            sys.exit(1)

    def is_enabled(self, name):
        dir = '/usr/lib/systemd/system/'
        path = os.path.join(dir, name)

        if os.path.exists(path):
            cmd = 'systemctl is-enabled ' + name
            ret, result = subprocess.getstatusoutput(cmd)
            if ret != 0:
                en, output = subprocess.getstatusoutput(f'systemctl enable {name}')
                if en !=0:
                    logger.error("systemd service enable failed")
                    sys.exit(1)

    def start(self, name):
        ret, result = subprocess.getstatusoutput(f'systemctl is-active {name}') 
        if ret == 0:
            reflag, re_output = subprocess.getstatusoutput(f'systemctl restart {name}')
            if reflag != 0:
                print(re_output)
                logger.error(f"{name} restart failed —— {re_output}")
                sys.exit(1)
        else:
            flag, output = subprocess.getstatusoutput(f'systemctl start {name}')
            if flag != 0:
                print(output)
                logger.error(f"{name} start failed —— {output}")
                sys.exit(1)
            else:
                logger.info(f"Start {name} success")
                print(f"Start {name} success")

    def stop(self, name):
        ret, result = subprocess.getstatusoutput(f'systemctl is-active {name}')
        if ret == 0:
            flag, output = subprocess.getstatusoutput(f'systemctl stop {name}')
            if flag == 0:
                logger.info(f"{name} stop success")
                print(f"{name} stop success")
                sys.exit(1)

    def disable(self, name):
        ret, result = subprocess.getstatusoutput(f'systemctl disable {name}')
        if ret != 0:
            print(f"{name} disable failed")
            logger.error(f"{name} disable failed")
            sys.exit(1)
        else:
            logger.info(f"{name} disable success")
            print(f"{name} disable success")


    def status(self, name):
        ret, result = subprocess.getstatusoutput(f'systemctl status {name}')
        print(result)

class service_aide:
    def aide_init(self):
        cmd = '`which aide` --init'
        ret, result = subprocess.getstatusoutput(cmd)
        if ret !=0:
            logger.error("Failed to initialize database")
            print("Failed to initialize database")
            sys.exit(1)
        lines = result.splitlines()
        for line in lines:
             if re.match('AIDE initialized database', line):
                 db_gz = line.split('AIDE initialized database at')
                 gz_file = db_gz[1].strip()
                 if len(gz_file) > 0:
                     flag, output = subprocess.getstatusoutput(f'cp -p {gz_file} /var/lib/aide/aide.db.gz')
                     if flag !=0:
                         logger.error("Failed to copy AIDE initialized database")
                         sys.exit(1)
                     else:
                         print( "Copy AIDE initialized database success")

    def aide_update(self):
        cmd = '`which aide` --update'
        ret, result = subprocess.getstatusoutput(cmd)
        if ret !=0:
            logger.error("Failed to update database")
            print("Failed to update database")
            sys.exit(1)
        lines = result.splitlines()
        for line in lines:
             if re.match('New AIDE database written to', line):
                 db_gz = line.split('New AIDE database written to')
                 gz_file = db_gz[1].strip()
                 if len(gz_file) > 0:
                     flag, output = subprocess.getstatusoutput(f'cp -p {gz_file} /var/lib/aide/aide.db.gz')
                     if flag !=0:
                         logger.error("Failed to copy AIDE initialized database")
                         sys.exit(1)
                     else:
                         print( "Copy AIDE initialized database success")




