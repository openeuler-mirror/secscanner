import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")



def S37_Kernelopps():
    set_kernel_oops = seconf.get('basic', 'set_kernel_oops')
    InsertSection("Set kernel panic on oops...")
    if set_kernel_oops == 'yes':
        if os.path.exists('/etc/sysctl.conf') and not os.path.exists('/etc/sysctl.conf_bak'):
            shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        if os.path.exists('/etc/rc.local') and not os.path.exists('/etc/rc.local_bak'):
            shutil.copy2('/etc/rc.local', '/etc/rc.local_bak')
        if os.path.exists('/lib/systemd/system/rc-local.service') and not os.path.exists('/lib/systemd/system/rc-local.service_bak'):
            shutil.copy2('/lib/systemd/system/rc-local.service', '/lib/systemd/system/rc-local.service_bak')

        if os.path.exists('/etc/sysctl.conf'):
            set_kerneloops = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                        set_kerneloops = 1
            if set_kerneloops == 0:
                with open('/etc/sysctl.conf', 'a') as add_file:
                    add_file.write('\nkernel.panic_on_oops=1\n')
            else:
                with open('/etc/sysctl.conf', 'w') as write_file:
                    for line in lines:
                        if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                            write_file.write('kernel.panic_on_oops=1\n')
                        else:
                            write_file.write(line)
            if os.path.exists('/etc/rc.local'):
                set_sysctl = False
                set_bash = False
                os.chmod('/etc/rc.local', 0o755)
                with open('/etc/rc.local', 'r') as read_file:
                    lines = read_file.readlines()
                    for line in lines:
                        if not re.match('#|$', line) and re.search('sysctl', line):
                            set_sysctl = True
                        if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                            set_bash = True

                if not set_sysctl:
                    with open('/etc/rc.local', 'a') as add_file:
                        add_file.write('\n/sbin/sysctl -p /etc/sysctl.conf\n')
                else:
                    pass

                if not set_bash:
                    with open('/etc/rc.local', 'a') as add_file:
                        add_file.write('\n#!/bin/sh -e\nkernel.panic_on_oops =1\nrm -rf /lib/systemd/system/ctrl-alt-del.target\nexit 0')
                else:
                    pass

                if os.path.exists('/lib/systemd/system/rc-local.service'):
                    multi_set = False
                    with open('/lib/systemd/system/rc-local.service', 'r') as read_file:
                        lines = read_file.readlines()
                        for line in lines:
                            if not re.match('#|$', line) and re.search('multi-user.target', line):
                                multi_set = True
                    if not multi_set:
                         with open('/lib/systemd/system/rc-local.service', 'a') as add_file:
                             add_file.write('\n[install]\nwantedBy=multi-user.target\n')
                    else:
                        pass
            else:
                pass

            sysrq_set = False
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                        sysrq_set = True
            
            rclocal_set = False
            with open('/etc/rc.local', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.panic_on_oops', line):
                        rclocal_set = True


            if sysrq_set and rclocal_set:
                logger.info("Set kernel panic on oops, checking ok")
                Display("- Set kernel panic on oops...", "FINISHED")
            else:
                logger.info("Set kernel panic on oops failed")
                Display("- Set kernel panic on oops...", "FAILED")
        else:
            logger.info("Set kernel panic on oops failed")
            Display("- No filepath /etc/sysctl.conf...", "FAILED")

    else:
        Display("- Skip set kernel panic on oops due to config file...", "SKIPPING")
