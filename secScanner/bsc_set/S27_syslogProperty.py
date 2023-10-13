import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
import pathlib
logger = logging.getLogger("secscanner")


def S27_syslogProperty():
    InsertSection("Change the log property...")
    SET_LOG_FILE_PROPERTY = seconf.get('advance', 'set_log_file_property')
    if SET_LOG_FILE_PROPERTY == 'yes':
        if not os.path.exists('/etc/rsyslog.conf_bak'):
            shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
        # -----------------------------------------------------
        # record original property of logfile
        pathlib.Path('/etc/secscanner.d/logfile_property').touch()
        logfile_pro = "/etc/secscanner.d/logfile_property"
        SYS_LOGFILE = []
        with open('/etc/rsyslog.conf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.search('/var/log', line) and (not re.match('#|$', line)):
                    temp = line.split()
                    if len(temp) == 2 and re.match('/var', temp[1]):
                        SYS_LOGFILE.append(temp[1])
        if len(logfile_pro) > 0:
            for i in SYS_LOGFILE:
                if os.path.exists(i):
                    SHELL_RUN = subprocess.run(['stat', '-c', '%a', i], stdout=subprocess.PIPE)
                    SHELL_OUT = SHELL_RUN.stdout
                    pro_val = SHELL_OUT.strip().decode()
                    with open(logfile_pro, 'a') as add_file:
                        add_file.write(f"\n{i}={pro_val}\n")

        # --------------change the log property--------------
        for ilog in SYS_LOGFILE:
            if os.path.exists(ilog):
                print(f"chmod {ilog} to 600")
                os.chmod(ilog, 0o600)

        logger.info("change the log file property successfully")
        Display("- Change the log file property...", "FINISHED")
    else:
        Display("- Skip change log file property due to config file...", "SKIPPING")
