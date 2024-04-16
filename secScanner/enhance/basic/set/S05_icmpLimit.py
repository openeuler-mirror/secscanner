import re
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import subprocess
logger = logging.getLogger("secscanner")

def S05_icmpLimit():
    InsertSection("Disable the icmp redirect...")
    disable_icmp_redirect = seconf.get('basic', 'disable_icmp_redirect')
    if disable_icmp_redirect == 'yes':
        if os.path.exists('/etc/sysctl.conf') and not os.path.exists('/etc/sysctl.conf_bak'):
            shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        if os.path.exists('/etc/sysctl.conf'):
            ACCEPT_REDIRECT_SET = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('accept_redirects', line):
                        ACCEPT_REDIRECT_SET = 1
            if ACCEPT_REDIRECT_SET == 0:
                with open('/etc/sysctl.conf', 'a') as add_file:
                    add_file.write('\nnet.ipv4.conf.all.accept_redirects=0\n')
            else:
                with open('/etc/sysctl.conf', 'w') as write_file:
                    for line in lines:
                        if not re.match('#|$', line) and re.search('accept_redirects', line):
                            write_file.write('net.ipv4.conf.all.accept_redirects=0\n')
                        else:
                            write_file.write(line)
            ret, result = subprocess.getstatusoutput('sysctl -p -q')
            if ret != 0:
                logger.warning('Command execution failed')

            IS_EXIST = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('accept_redirects', line):
                        IS_EXIST = 1
            if IS_EXIST == 1:
                logger.info("Set the icmp redirect, checking ok")
                Display("- Set the icmp redirect...", "FINISHED")
            else:
                logger.info("Set the icmp redirect failed")
                Display("- Set the icmp redirect...", "FAILED")
        else:
            logger.info("Set the icmp redirect failed")
            Display("- No filepath /etc/sysctl.conf...", "FAILED")
    else:
        Display("- Skip disable the icmp redirect due to config file...", "SKIPPING")
