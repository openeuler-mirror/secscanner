import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import shutil


def S26_disableUnUsedaliases():
    InsertSection("set disable the unused aliases...")
    Display(f"- Skip disable the unused aliases, due to config file...", "SKIPPING")



