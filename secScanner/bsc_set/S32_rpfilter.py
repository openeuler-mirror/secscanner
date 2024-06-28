import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S32_rpfilter():
    set_rp_filter = seconf.get('basic', 'set_rp_filter')
    InsertSection("Set the reverse path filtering...")
    if set_rp_filter == 'yes':
        if os.path.exists('/etc/sysctl.conf') and not os.path.exists('/etc/sysctl.conf_bak'):
            shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        add_bak_file('/etc/sysctl.conf_bak')
        if os.path.exists('/etc/sysctl.conf'):
            rp_filter = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('rp_filter', line):
                        rp_filter = 1
            if rp_filter == 0:
                with open('/etc/sysctl.conf', 'a') as add_file:
                    add_file.write('\nnet.ipv4.conf.all.rp_filter=1\n')
                    add_file.write('\nnet.ipv4.conf.default.rp_filter=1\n')
            else:
                with open('/etc/sysctl.conf', 'w') as write_file:
                    for line in lines:
                        if not re.match('#|$', line) and re.search('rp_filter', line):
                            write_file.write('net.ipv4.conf.all.rp_filter=1\n')
                            write_file.write('net.ipv4.conf.default.rp_filter=1\n')
                        else:
                            write_file.write(line)

            ret, result = subprocess.getstatusoutput('sysctl -p -q')
            if ret != 0:
                logger.warning('Command execution failed')

            IS_EXIST = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('rp_filter', line):
                        IS_EXIST = 1
            if IS_EXIST == 1:
                logger.info("Set the reverse path filtering, checking ok")
                Display("- Set the reverse path filtering...", "FINISHED")
            else:
                logger.info("Set the reverse path filtering failed")
                Display("- Set the reverse path filtering...", "FAILED")
        else:
            logger.info("Set the reverse path filtering failed")
            Display("- No filepath /etc/sysctl.conf...", "FAILED")

    else:
        Display("- Skip disable the reverse path filtering due to config file...", "SKIPPING")
