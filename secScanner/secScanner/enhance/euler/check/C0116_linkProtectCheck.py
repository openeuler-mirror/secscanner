import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_euler import *
logger = logging.getLogger("secscanner")

def C0116_linkProtectCheck():
    '''
    Function: Check whether the soft and hard link file protection is enabled
    '''
    InsertSection("Check whether link file protection is enabled")
    linkTypes = ["symlinks", "hardlinks"]
    warnMessage = [WRN_C0116_01, WRN_C0116_02]
    sugMessage = [SUG_C0116_01, SUG_C0116_02]

    for i in range(len(linkTypes)):
        linkType = linkTypes[i]
        protectFlag = "fs.protected_%s" % linkType
        result_symlinks = subprocess.run(['sysctl', protectFlag], capture_output=True)
        resultStr = result_symlinks.stdout.strip().decode("utf-8")
        if resultStr[-1] == '0':
            with open(RESULT_FILE, "a") as file:
                file.write("\nC0116\n")
            logger.warning("WRN_C0116_0%d: %s", (i + 1), warnMessage[i])
            logger.warning("SUG_C0116_0%d: %s", (i + 1), sugMessage[i])
            Display("- %s protection is disabled..." % linkType, "WARNING")
        else:
            logger.info("Link type (%s) protection is enabled", linkType)
            Display("- Check whether %s fileprotection is enabled..." % linkType, "OK")
