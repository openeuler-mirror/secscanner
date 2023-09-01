import logging
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
from secScanner.commands.check_outprint import *

def C21_issueRemove():
    logger = logging.getLogger("secscanner")
    InsertSection("check the issue file")
    ISVIRTUALMACHINE = get_value("ISVIRTUALMACHINE")
    if ISVIRTUALMACHINE != 1:
        if os.path.exists("/etc/issue"):
            with open(RESULT_FILE, "a") as file:
                file.write("\nC21\n")
            logger.warning("WRN_C21 :%s",WRN_C21)
            logger.info("Suggestion: %s", SUG_C21)
            Display("- Check if there is issue file...", "WARNING")
        else:
            logger.info("There is no issue file remain, check ok")
            Display("- Check if there is issue file...", "OK")
    else:
        logger.info("This is virtual machine, can't remove the issue file")
        Display("- Check if there is issue file...", "SKIPPED")
        Display("- This is virtual machine, can't remove the issue file", '')




