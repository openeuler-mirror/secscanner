import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil

logger = logging.getLogger("secscanner")


def S16_lockUnUsedUser():
    InsertSection("Lock the unused users...")
    SET_DISABLE_UNUSED_USER = seconf.get('basic', 'disable_unused_user')
    UNUSED_USER_VALUE = seconf.get('basic', 'unused_user_value').split()

    if SET_DISABLE_UNUSED_USER == 'yes':
        for i in UNUSED_USER_VALUE:
            #print(f"lock user: {i}")
            subprocess.run(['usermod', '-L', '-s', '/bin/false', i], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("lock the unused user successfully")
        Display("- lock the unused user ...", "FINISHED")
    else:
        Display("- Skip lock the unused users, due to config file...", "SKIPPING")
