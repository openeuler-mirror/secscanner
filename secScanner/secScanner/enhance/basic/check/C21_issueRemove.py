import logging
from secScanner.lib import *
from secScanner.commands.check_outprint import *
logger = logging.getLogger("secscanner")

def C21_issueRemove():
    InsertSection("check the issue file")
    ISVIRTUALMACHINE = get_value("ISVIRTUALMACHINE")
    if ISVIRTUALMACHINE != 1:
        if os.path.exists("/etc/issue") and os.path.exists("/etc/issue.net"):
            with open(RESULT_FILE, "a") as file:
                file.write("\nC21\n")
            logger.warning("WRN_C21 :%s", WRN_C21)
            logger.warning("SUG_C21: %s", SUG_C21)
            Display("- Check if there is issue file...", "WARNING")
        else:
            logger.info("There is no issue file remain, check ok")
            Display("- Check if there is issue file...", "OK")
    else:
        logger.info("This is virtual machine, can't remove the issue file")
        Display("- This is virtual machine, can't remove the issue file", 'SKIPPED')




