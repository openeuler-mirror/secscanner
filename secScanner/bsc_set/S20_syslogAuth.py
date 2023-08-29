import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
def S20_syslogAuth():
    logger = logging.getLogger("secscanner")
    SET_RECORDING_AUTH_EVENTS = seconf.get('basic', 'recording_auth_events')
    AUTH_EVENTS_FILE_NAME = seconf.get('basic', 'auth_events_file_name')
    InsertSection("Recording the auth events...")
    if SET_RECORDING_AUTH_EVENTS == 'yes':
        if os.path.exists('/etc/rsyslog.conf'):
            if not os.path.exists('/etc/rsyslog.conf_bak'):
                shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
        if os.path.exists('/etc/syslog.conf'):
            if not os.path.exists('/etc/syslog.conf_bak'):
                shutil.copy2('/etc/syslog.conf', '/etc/syslog.conf_bak')
        IS_EXIST = 0
        with open('/etc/rsyslog.conf', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if  re.match('auth.none', line) and re.search('/var/log', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/rsyslog.conf', 'a') as add_file:
                add_file.write(f"\nauth.none /var/log/{AUTH_EVENTS_FILE_NAME}\n")
        else:
            logger.info("has auth.none set, passing...")
        Display(f"- Setting the rsyslog.conf, recording the auth events...", "FINISHED")
    else:
        Display(f"- Skip recording the auth events due to config file...", "SKIPPING")