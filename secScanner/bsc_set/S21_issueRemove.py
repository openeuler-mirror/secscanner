import subprocess
import shutil
import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil
def S21_issueRemove():
    HIDE_ISSUE_INFO = seconf.get('advance', 'hide_issue_info')
    logger = logging.getLogger("secscanner")
    InsertSection("Remove the issue.net and issue file")
    if HIDE_ISSUE_INFO == 'yes':
        if ISVIRTUALMACHINE != 1:
            if os.path.exists('/etc/issue'):
                shutil.copy2('/etc/issue', '/etc/issue_bak')
                shutil.copy2('/etc/issue.net', '/etc/issue.net_bak')
                if os.path.isfile('/etc/issue'):
                    os.remove('/etc/issue')
                if os.path.isfile('/etc/issue.net'):
                    os.remove('/etc/issue.net')

            if os.path.exists('/etc/issue'):
                logger.info("Still remain issue file, setting failed")
                Display("- Remove the issue file...", "FAILED")
            else:
                logger.info("There is no issue file remain, setting ok")
                Display("- Remove the issue file...", "FINISHED")

        else:
            logger.info("This is virtual machine, can't remove the issue file")
            Display("- Remove the issue file...", "SKIPPED")
            Display("- This is virtual machine, can't remove the issue file")
    else:
        Display("- Skip hide issue file due to config file...", "SKIPPING")
