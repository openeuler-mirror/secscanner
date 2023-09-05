import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C10_sshBanner():
    logger = logging.getLogger("secscanner")

    InsertSection("check the ssh_banner")
    TMP_V = 0
    if os.path.exists("/etc/sshbanner"):
        with open("/etc/ssh/sshd_config", "r") as file:
            lines = file.readlines()
            for line in lines:
                if re.match('Banner', line) and re.match('/etc/sshbanner', line) and (not re.match('^#|^$', line)):
                    TMP_V = TMP_V + 1
        if TMP_V > 0:
            logger.info("Has sshbanner set, checking ok")
            Display("- Check the sshbanner...", "OK")
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
