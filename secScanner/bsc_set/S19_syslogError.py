import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
def S19_syslogError():
    logger = logging.getLogger("secscanner")
    SET_RECORDING_ERROR_EVENTS = seconf.get('basic', 'recording_error_events')
    ERROR_FILE_NAME = seconf.get('basic', 'error_file_name')
    InsertSection("Recording the error events...")
    if SET_RECORDING_ERROR_EVENTS == 'yes':
        if not os.path.exists('/etc/rsyslog.conf_bak'):
            shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
        IS_EXIST = 0
        with open('/etc/rsyslog.conf', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if  re.match('\*\.err', line) and re.search('/var/log', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/rsyslog.conf', 'a') as add_file:
                add_file.write(f"\n*.err /var/log/{ERROR_FILE_NAME}\n")
        else:
            logger.info("has *.err set, passing...")
        Display(f"- Setting the rsyslog.conf, recording the error events...", "FINISHED")
    else:
        Display(f"- Skip recording the error events due to config file...", "SKIPPING")