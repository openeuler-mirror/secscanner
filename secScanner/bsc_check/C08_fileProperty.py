import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")


def C08_fileProperty():
    InsertSection("check file property set")
    BASIC_OPTIONS = seconf.options('basic')  # search basic and show all options
    CHMOD_644_FILE = []
    CHMOD_600_FILE = []
    CHMOD_400_FILE = []
    CHMOD_751_FILE = []
    CHMOD_750_FILE = []  # declare variable just in case
    if 'chmod_644_file' in BASIC_OPTIONS:  # if there is a 'chmod 644 file', save the value in a list
        CHMOD_644_FILE = seconf.get('basic', 'chmod_644_file').split()
    if 'chmod_600_file' in BASIC_OPTIONS:
        CHMOD_600_FILE = seconf.get('basic', 'chmod_600_file').split()
    if 'chmod_400_file' in BASIC_OPTIONS:
        CHMOD_400_FILE = seconf.get('basic', 'chmod_400_file').split()
    if 'chmod_751_file' in BASIC_OPTIONS:
        CHMOD_751_FILE = seconf.get('basic', 'chmod_751_file').split()
    if 'chmod_750_file' in BASIC_OPTIONS:
        CHMOD_750_FILE = seconf.get('basic', 'chmod_750_file').split()
    tmp_count = 1  # count the number of WARN_C08_tmp_count
    for i in CHMOD_644_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
            if file_permission == '644':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC08\n")
                warn_str = "WRN_C08_" + str(tmp_count)
                sugs_str = "SUG_C08_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1

    for i in CHMOD_600_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]
            if file_permission == '600':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC08\n")
                warn_str = "WRN_C08_" + str(tmp_count)
                sugs_str = "SUG_C08_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1

    for i in CHMOD_400_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]
            if file_permission == '400':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC08\n")
                warn_str = "WRN_C08_" + str(tmp_count)
                sugs_str = "SUG_C08_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1

    for i in CHMOD_751_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]
            if file_permission == '751':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC08\n")
                warn_str = "WRN_C08_" + str(tmp_count)
                sugs_str = "SUG_C08_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1

    for i in CHMOD_750_FILE:
        if os.path.exists(i):
            file_permission = oct(os.stat(i).st_mode)[-3:]
            if file_permission == '750':
                logger.info(f"{i} is safe, checking ok")
                Display(f"- Check {i} property...", "OK")
            else:
                with open(RESULT_FILE, "a") as file:
                    file.write("\nC08\n")
                warn_str = "WRN_C08_" + str(tmp_count)
                sugs_str = "SUG_C08_" + str(tmp_count)
                logger.warning(f"{warn_str}: %s", eval(warn_str))
                logger.warning(f"{sugs_str}: %s", eval(sugs_str))
                Display(f"- {i}'s property is not safe...", "WARNING")
            tmp_count = tmp_count + 1
