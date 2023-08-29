import logging
import os
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C25_addUser():
    logger = logging.getLogger("secscanner")
    InsertSection("check whether have the customer user")
    count_user = 0
    ADV_OPTIONS = seconf.options('advance')#search basic and show all options
    USER_NAME = ''
    if ('username' in ADV_OPTIONS):# if there is a 'userName', save the value
        USER_NAME = seconf.get('advance', 'username')

    with open('/etc/passwd', 'r') as file:
        lines = file.readlines()
        for line in lines:
            temp = line.split(':', -1)
            if temp[0] == USER_NAME:
                count_user = count_user + 1
    if USER_NAME == '':
        logger.info("No vaild userName found, please check config file...")
        Display("--indent 2 --text - No vaild userName found, please check config file...  --result FAILED --color RED")
    else:
        if count_user == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC25\n")
            logger.info(f"WRN_C25: %s :", WRN_C25)
            logger.warning("Suggestion: %s", SUG_C25)
            Display("- Check whether have additional user..." "WARNING")
            Display("- No additional user found, check warning")
        else:
            logger.info(f"Already have {USER_NAME}, no need to add")
            Display(f"- Already have {USER_NAME}...", "OK")



