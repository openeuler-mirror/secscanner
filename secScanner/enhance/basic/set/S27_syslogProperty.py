import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
import pathlib
logger = logging.getLogger("secscanner")


def S27_syslogProperty():
    InsertSection("Change the log property...")
    set_log_file_property = seconf.get('advance', 'set_log_file_property')
    if set_log_file_property == 'yes':
        if os.path.exists('/etc/rsyslog.conf'):
            if not os.path.exists('/etc/rsyslog.conf_bak'):
                shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
            # -----------------------------------------------------
            # record original property of logfile
            pathlib.Path('/etc/secscanner.d/logfile_property').touch()
            logfile_pro = "/etc/secscanner.d/logfile_property"
            sys_logfile = []
            with open('/etc/rsyslog.conf', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if re.search('/var/log', line) and (not re.match('#|$', line)):
                        temp = line.split()
                        if len(temp) == 2 and re.match('/var', temp[1]):
                            sys_logfile.append(temp[1])
            if len(logfile_pro) > 0:
                for i in sys_logfile:
                    if os.path.exists(i):
                        ret, result = subprocess.getstatusoutput(f'stat -c %a {i}')
                        if ret != 0:
                            logger.warning('Command execution failed')
                            Display("- Command execution failed...", "FAILED")
                        with open(logfile_pro, 'a') as add_file:
                            add_file.write(f"\n{i}={result}\n")

            # --------------change the log property--------------
            for ilog in sys_logfile:
                if os.path.exists(ilog):
                    #print(f"chmod {ilog} to 600")
                    os.chmod(ilog, 0o600)

            logger.info("change the log file property successfully")
            Display("- Change the log file property...", "FINISHED")
        else:
            Display("- file '/etc/rsyslog.conf' does not exist...", "SKIPPED")
    else:
        Display("- Skip change log file property due to config file...", "SKIPPING")
