import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil

logger = logging.getLogger("secscanner")


def S16_lockUnUsedUser():
    InsertSection("Lock the unused users...")
    set_disable_unused_user = seconf.get('basic', 'disable_unused_user')
    unused_user_value = seconf.get('basic', 'unused_user_value').split()

    if set_disable_unused_user == 'yes':
        for i in unused_user_value:
            ret, result = subprocess.getstatusoutput(f'usermod -L -s /bin/false {i}')
            if ret != 0:
                logger.warning(f'{result}')

        logger.info("lock the unused user successfully")
        Display("- lock the unused user ...", "FINISHED")
    else:
        Display("- Skip lock the unused users, due to config file...", "SKIPPING")
