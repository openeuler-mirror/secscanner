import logging
import os
import subprocess
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C16_lockUnUsedUser():
    InsertSection("check the unused user")
    unuser_user = seconf.get('basic', 'unused_user_value').split()
    #UnUsed = ['adm', 'lp', 'sync', 'shutdown', 'halt', 'news', 'uucp', 'operator', 'games', 'nobody', 'rpm', 'smmsp']
    error_user = []
    counter = 0

    for i in unuser_user:
        try:
            output = subprocess.check_output(["grep", "-i", f"^{i}:", "/etc/shadow"])
            output = output.decode("utf-8").strip()
            password_field = output.split(':')[1] if ':' in output else None

            if password_field is not None and not password_field.startswith(('!', '*')):
                error_user.append(i)
                counter += 1
        except subprocess.CalledProcessError:
            pass

        except Exception as e:
            print(f"An error occurred: {e}")

    if counter > 0:
        with open(RESULT_FILE, "a") as file:
            file.write("\nC16\n")
        logger.warning(f"WRN_C16: These users: {error_user} should lock")
        logger.warning("SUG_C16: %s", SUG_C16)
        Display("- Check if there have unused user...", "WARNING")
    else:
        logger.info("All unused user is locked, checking ok")
        Display("- Check if there have unused user...", "OK")
