import logging
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import WRN_C07_01, WRN_C07_02, SUG_C07
import re
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def C07_TMOUT():
    InsertSection("check the TMOUT set")
    with open("/etc/profile", "r") as file:
        lines = file.readlines()
        IS_EXIST = sum(1 for line in lines if not re.match('^#|^$', line) and "TMOUT=" in line)

    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC07\n")
        logger.warning("WRN_C07_01: %s", WRN_C07_01)
        logger.warning("SUG_C07: %s", SUG_C07)
        Display("- No TMOUT set...", "WARNING")
    else:
        for line in lines:
            if (not re.match('^#|^$', line)) and "TMOUT=" in line:
                regex = r'(?<=TMOUT=).[0-9]*'
                TMO = re.findall(regex, line)
                if not TMO:
                    Display("--indent 2 --text - No TMOUT set...  --result WARNING --color RED")
                elif TMO[0] > str(300):
                    with open(RESULT_FILE, "a") as file:
                        file.write("\nC07\n")
                    logger.warning("WRN_C07_02: %s", WRN_C07_02)
                    logger.warning("SUG_C07: %s", SUG_C07)
                    Display("- Wrong TMOUT set, must less than 300...", "WARNING")
                else:
                    logger.info("Has right TMOUT set, checking ok")
                    Display("- Has right TMOUT set ...", "OK")
