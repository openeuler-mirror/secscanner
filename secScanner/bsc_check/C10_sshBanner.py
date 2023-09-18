import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
logger = logging.getLogger("secscanner")


def C10_sshBanner():
    InsertSection("check the ssh banner")
    TMP_V = False
    if os.path.exists("/etc/sshbanner"):
        with open("/etc/ssh/sshd_config", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.search('Banner', line) and re.search('/etc/sshbanner', line) and (not re.match('^#|^$', line)):
                    TMP_V = True
        if TMP_V:
            logger.info("Has ssh banner set, checking ok")
            Display("- Check the ssh banner...", "OK")
        else:
            logger.warning("WRN_C10_01: %s", WRN_C10_01)
            logger.warning("SUG_C10: %s", SUG_C10)
            Display("- No ssh banner config set...", "WARNING")
    else:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC10\n")
        logger.warning("WRN_C10_02: %s", WRN_C10_02)
        logger.warning("SUG_C10: %s", SUG_C10)
        Display("- No sshbanner file...", "WARNING")
