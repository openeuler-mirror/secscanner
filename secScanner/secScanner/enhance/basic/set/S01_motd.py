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


import shutil
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")


def S01_motd():
    InsertSection("set /etc/motd banner")
    set_motd = seconf.get('basic', 'set_motd')
    motd = seconf.get('basic', 'motd')
    if set_motd == 'yes':
        if os.path.exists('/etc/motd') and not os.path.exists('/etc/motd_bak'):
            shutil.copy2('/etc/motd', '/etc/motd_bak')
        add_bak_file('/etc/motd_bak')
        if not os.path.exists('/etc/motd'):
            pathlib.Path('/etc/motd').touch()
            os.chmod('/etc/motd', 600)
        if os.path.exists('/etc/motd'):
            with open('/etc/motd', "w") as write_file:
                write_file.write(motd)
            if os.path.getsize('/etc/motd'):
                logger.info("set the motd banner successfully")
                Display("- Set motd banner finished...", "FINISHED")
    else:
        Display("- Skip set motd banner due to config file...", "SKIPPING")



