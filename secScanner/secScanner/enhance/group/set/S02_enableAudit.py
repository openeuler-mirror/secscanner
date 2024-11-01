import sys
import shutil
from secScanner.lib import *
from secScanner.gconfig import *
import logging
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")

#1.(3)5.1)保证审计机制默认处于开启状态，且对审计日志的开启和关闭进行保护
enable_aduit = seconf.get('group', 'enable_aduit')

