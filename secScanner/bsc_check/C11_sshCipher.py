import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C11_sshCipher():
    logger = logging.getLogger("secscanner")

    InsertSection("check the ssh_cipher")
    IS_EXIST = 0
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('Ciphers', line) and (not re.match('^#|^$', line)):
                IS_EXIST = IS_EXIST + 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC11\n")
        logger.warning("WRN_C11: %s", WRN_C11)
        logger.warning("Suggestion: %s", SUG_C11)
        Display("- No ssh cipher config set...", "WARNING")
    else:
        logger.info("Has ssh cipher set, checking ok")
        Display("- Check the ssh cipher...", "OK")

