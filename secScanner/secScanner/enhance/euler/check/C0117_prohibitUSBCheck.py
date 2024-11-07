import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_euler import *
logger = logging.getLogger("secscanner")

def C0117_prohibitUSBCheck():
    '''
    Function: Check whether the prohibition of USB devices is enabled
    '''
    InsertSection("Check whether the prohibition of USB devices  is enabled")
    warnMessage = WRN_C0117
    sugMessage = SUG_C0117

    result = subprocess.run(["modprobe", "-n", "-v", "usb-storage"], capture_output=True)
    resultStr = result.stdout.strip().decode("utf-8")
    if resultStr == "install /bin/true":
        logger.info("The prohibition of USB devices is enabled")
        Display("- Check whether the prohibition of USB devices is enabled...", "OK")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC0117\n")
        logger.warning("WRN_C0117: %s", warnMessage) 
        logger.warning("SUG_C0117: %s", sugMessage)
        Display("- The Prohibition of USB devices is disabled...", "WARNING")
