import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
logger = logging.getLogger("secscanner")


def S17_syslogLogin():
    InsertSection("Recording the login events...")
    SET_RECORDING_LOGIN_EVENTS = seconf.get('basic', 'recording_login_events')
    LOGIN_EVENTS_FILE_NAME = seconf.get('basic', 'login_events_file_name')

    if SET_RECORDING_LOGIN_EVENTS == 'yes':
        if os.path.exists('/etc/rsyslog.conf') and not os.path.exists('/etc/rsyslog.conf_bak'):
                shutil.copy2('/etc/rsyslog.conf', '/etc/rsyslog.conf_bak')
        if os.path.exists('/etc/rsyslog.conf'):
            IS_EXIST = 0
            with open('/etc/rsyslog.conf', 'r') as read_file:
                lines = read_file.readlines()
                for line in lines:
                    if re.match('authpriv.info', line) and re.search('/var/log', line):
                        IS_EXIST = 1
            if IS_EXIST == 0:
                with open('/etc/rsyslog.conf', 'a') as add_file:
                    add_file.write(f"\nauthpriv.info /var/log/{LOGIN_EVENTS_FILE_NAME}\n")
            else:
                logger.info("has authpriv.info set, passing...")
            Display("- Setting the rsyslog.conf, recording the login events...", "FINISHED")
        else:
            logger.info("no filepath /etc/rsyslog.conf")
            Display("- no filepath /etc/rsyslog.conf...", "SKIPPING")
    else:
        Display("- Skip recording login events due to config file...", "SKIPPING")
