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


def S0228_warnBanner():
    InsertSection("set system warning banner")
    set_banner = seconf.get('euler', 'set_banner')
    motd = seconf.get('euler', 'motd')
    issue = seconf.get('euler', 'issue')
    issue_content = issue.replace('\\n', '\n')

    if set_banner == 'yes':
        if os.path.exists('/etc/motd') and not os.path.exists('/etc/motd_bak'):
            shutil.copy2('/etc/motd', '/etc/motd_bak')
        add_bak_file('/etc/motd_bak')
        if not os.path.exists('/etc/motd'):
            pathlib.Path('/etc/motd').touch()
            os.chmod('/etc/motd', 644)
        if os.path.exists('/etc/motd'):
            with open('/etc/motd', "w") as write_file:
                write_file.write(motd)
            if os.path.getsize('/etc/motd'):
                logger.info("set the motd banner successfully")
                Display("- Set motd banner finished...", "FINISHED")

        if os.path.exists('/etc/issue') and not os.path.exists('/etc/issue_bak'):
            shutil.copy2('/etc/issue', '/etc/issue_bak')
        add_bak_file('/etc/issue_bak')
        if not os.path.exists('/etc/issue'):
            pathlib.Path('/etc/issue').touch()
            os.chmod('/etc/issue', 644)
        if os.path.exists('/etc/issue'):
            with open('/etc/issue', "w") as write_file:
                write_file.write(issue_content)
            if os.path.getsize('/etc/issue'):
                logger.info("set the /etc/issue banner successfully")
                Display("- Set /etc/issue banner finished...", "FINISHED")

        if os.path.exists('/etc/issue.net') and not os.path.exists('/etc/issue.net_bak'):
            shutil.copy2('/etc/issue.net', '/etc/issue.net_bak')
        add_bak_file('/etc/issue.net_bak')
        if not os.path.exists('/etc/issue.net'):
            pathlib.Path('/etc/issue.net').touch()
            os.chmod('/etc/issue.net', 644)
        if os.path.exists('/etc/issue.net'):
            with open('/etc/issue.net', "w") as write_file:
                write_file.write(issue_content)
            if os.path.getsize('/etc/issue.net'):
                logger.info("set the /etc/issue.net banner successfully")
                Display("- Set /etc/issue.net banner finished...", "FINISHED")

    else:
        Display("- Skip set system warning banner due to config file...", "SKIPPING")



