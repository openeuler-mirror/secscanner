import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
logger = logging.getLogger("secscanner")


def S36_disMagicKeys():
    set_disable_magickeys = seconf.get('basic', 'set_disable_magickeys')
    InsertSection("Set disable magic keys...")
    if set_disable_magickeys == 'yes':
        if os.path.exists('/etc/sysctl.conf') and not os.path.exists('/etc/sysctl.conf_bak'):
            shutil.copy2('/etc/sysctl.conf', '/etc/sysctl.conf_bak')
        add_bak_file('/etc/sysctl.conf_bak')

        if os.path.exists('/etc/sysctl.conf'):
            sysrq = 0
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.sysrq', line):
                        sysrq = 1
            if sysrq == 0:
                with open('/etc/sysctl.conf', 'a') as add_file:
                    add_file.write('\nkernel.sysrq=0\n')
            else:
                with open('/etc/sysctl.conf', 'w') as write_file:
                    for line in lines:
                        if not re.match('#|$', line) and re.search('kernel.sysrq', line):
                            write_file.write('kernel.sysrq=0\n')
                        else:
                            write_file.write(line)
            ret, result = subprocess.getstatusoutput('sysctl -p -q')
            if ret != 0:
                logger.warning('Command execution failed')        

            sysrq_set = False
            with open('/etc/sysctl.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if not re.match('#|$', line) and re.search('kernel.sysrq', line):
                        sysrq_set = True

            if sysrq_set:
                logger.info("Set disable magic keys, checking ok")
                Display("- Set disable magic keys...", "FINISHED")
            else:
                logger.info("Set disable magic keys failed")
                Display("- Set disable magic keys...", "FAILED")
        else:
            logger.info("Set disable magic keys failed")
            Display("- No filepath /etc/sysctl.conf...", "FAILED")

    else:
        Display("- Skip set disable magic keys due to config file...", "SKIPPING")
