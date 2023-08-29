import logging
import os
import subprocess
from subprocess import PIPE
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")
###dont know how to solve error in subprocess.run
def C29_sysUpdate():
    InsertSection("check the system update info")
    SHELL_RUN = subprocess.run(['yum', 'check-update'],timeout=10, stdout = PIPE)
    SHELL_RESULT = SHELL_RUN.stdout # get shell result, SHELL_RESULT is a stream of bytes
    temp = SHELL_RESULT.split(b'\n', -1) #cut the byte stream by lines
    UPDATE_COUNT = 0
    for i in range(len(temp)):
        line_list = temp[i].split()#delete space and split
        if len(line_list) == 3:
            # len(line_list) means this line contains [software.x86_64, version, BaseOS]
            UPDATE_COUNT = UPDATE_COUNT + 1
    if UPDATE_COUNT > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC29\n")
        logger.info(f"WRN_C29: There are {UPDATE_COUNT} softwares need updating")
        logger.warning("Suggestion: %s", SUG_C29_01)
        Display(f"- {UPDATE_COUNT} packages can be updated...", "WARNING")
        Display(f"- Note: type 'yum check-update' to see update information.")
    else:
        logger.info("No software need to update, checking ok")
        Display("- No software need update...", "OK")
