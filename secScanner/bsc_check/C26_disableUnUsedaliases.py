import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C26_disableUnUsedaliases():
    InsertSection("check disable the unused aliases")
    Display("- Check if unused aliases are locked...", "SKIPPING")

