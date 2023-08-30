import logging
import os
import re
import subprocess
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C30_softwareBugs():
    logger = logging.getLogger("secscanner")
    InsertSection("check the software vulnerabilities")
