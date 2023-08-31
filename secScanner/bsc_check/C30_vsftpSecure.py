import logging
import os
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

def C30_vsftpSecure():
    logger = logging.getLogger("secscanner")
    InsertSection("check the vsftp configuration")
    if os.path.exists("/etc/vsftpd/vsftpd.conf"):
        ANONYMOUS_SET = 0
        FTPD_BANNER_SET = 0
        USERLIST_SET = 0
        with open("/etc/vsftpd/vsftpd.conf", 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.match("anonymous_enable=NO", line):
                    ANONYMOUS_SET = 1
                if re.search("ftpd_banner", line) and not re.match("#|$", line):
                    FTPD_BANNER_SET = 1
                if re.match("userlist_enable=YES", line):
                    USERLIST_SET = 1
        FTP_UESRS_SET = 0
        with open("/etc/vsftpd/ftpusers", 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if re.search("root", line) and not re.match("#|$", line):
                    FTP_UESRS_SET = 1
        if ANONYMOUS_SET == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC23 anonymous_enable\n")
            logger.info(f"WRN_C23_01: %s :", WRN_C30_01)
            logger.warning("Suggestion: %s", SUG_C30_01)
            Display("- Check vsftpd anonymous_enable setting...", "WARNING")
            Display("- anonymous_enable is not set to 'NO', check warning...")
        else:
            logger.info("The vsftpd's anonymous_enable is NO, check OK")
            Display("- Check vsftpd anonymous_enable setting...", "OK")

        if FTPD_BANNER_SET == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC23 ftp_banner\n")
            logger.info(f"WRN_C23_02: %s :", WRN_C30_02)
            logger.warning("Suggestion: %s", SUG_C30_02)
            Display("- Check vsftpd ftp_banner setting...", "WARNING")
            Display("- anonymous_enable is not set, check warning...")
        else:
            logger.info("has ftpd_banner set, passing")
            Display("- Check vsftpd ftp_banner setting...", "OK")

        if USERLIST_SET == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC23 userlist_enable\n")
            logger.info(f"WRN_C23_03: %s :", WRN_C30_03)
            logger.warning("Suggestion: %s", SUG_C30_03)
            Display("- Check vsftpd userlist_enable setting...", "WARNING")
            Display("- userlist_enable is not set to 'YES', check warning...")
        else:
            logger.info("The vsftpd's userlist_enable is YES, check OK")
            Display("- Check vsftpd userlist_enable setting...", "OK")

        if FTP_UESRS_SET == 0:
            with open(RESULT_FILE, "a") as file:
                file.write("\nC23 ftpusers\n")
            logger.info(f"WRN_C23_04: %s :", WRN_C30_04)
            logger.warning("Suggestion: %s", SUG_C30_04)
            Display("- Check vsftpd ftpusers setting...", "WARNING")
            Display("- userlist_enable is not set to 'YES', check warning...")
        else:
            logger.info("The ftpusers config file contains user:root set, check ok")
            Display("- Check vsftpd ftpusers setting...", "OK")

    else:
        logger.info("/etc/vsftpd/vsftpd.conf not found, or it does not installed")
        Display("- No vsftpd.conf found, maybe vsftp not installed...", "SKIPPED")
