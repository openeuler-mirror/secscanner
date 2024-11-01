import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")


def C11_sshAlgorithms():
    InsertSection("check the ssh algorithms")
    IS_EXIST = 0
    with open("/etc/ssh/sshd_config", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('KexAlgorithms', line) and (not re.match('^#|^$', line)):
                IS_EXIST = IS_EXIST + 1
            elif re.match('Ciphers', line) and (not re.match('^#|^$', line)):
                IS_EXIST = IS_EXIST + 1
            elif re.match('MACs', line) and (not re.match('^#|^$', line)):
                IS_EXIST = IS_EXIST + 1
    if IS_EXIST == 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC11\n")
        logger.warning("WRN_C11: %s", WRN_C11)
        logger.warning("SUG_C11: %s", SUG_C11)
        Display("- No ssh algorithms config set...", "WARNING")
    else:
        logger.info("Has ssh algorithms set, checking ok")
        Display("- Check the ssh algorithms...", "OK")

