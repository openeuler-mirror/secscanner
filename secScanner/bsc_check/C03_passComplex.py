import logging
import re
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *
def C03_passComplex():
    logger = logging.getLogger("secscanner")

    # only one minlen minclass ...count don't need
    regex_minlen = r'(?<=minlen=).[0-9]*'
    regex_minclass = r'(?<=minclass=).[0-9]*'
    regex_ucredit = r'(?<=ucredit=).[0-9]*'
    regex_lcredit = r'(?<=lcredit=).[0-9]*'
    regex_dcredit = r'(?<=dcredit=).[0-9]*'
    regex_ocredit = r'(?<=ocredit=).[0-9]*'
    t_minlen = '' #if not match minlen, t_minlen= ''
    t_minclass = ''
    n_ucredit = ''
    n_lcredit = ''
    n_dcredit = ''
    n_ocredit = ''

    # search part
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('minlen=', line) and (not re.match('#', line)):
                temp = re.findall(regex_minlen, line)
                if temp != []:
                    t_minlen = temp[0] # must found num,  if temp == [] means no number after "minlen" No password set
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('minclass=', line) and (not re.match('#', line)):
                temp = re.findall(regex_minclass, line)
                if temp != []:
                    t_minclass = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('ucredit=', line) and (not re.match('#', line)):
                temp = re.findall(regex_ucredit, line)
                if temp != []:
                    n_ucredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('lcredit=', line) and (not re.match('#', line)):
                temp = re.findall(regex_lcredit, line)
                if temp != []:
                    n_lcredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('dcredit=', line) and (not re.match('#', line)):
                temp = re.findall(regex_dcredit, line)
                if temp != []:
                    n_dcredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('ocredit=', line) and (not re.match('#', line)):
                temp = re.findall(regex_ocredit, line)
                if temp != []:
                    n_ocredit = temp[0]

    # decide part
    InsertSection("check passwd minlen set")
    # ------------------------------------------------------------------------------------------------
    if t_minlen == '':
        # minlen not found or no numbers after minlen
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_02: %s", WRN_C03_02)
        logger.warning("Suggestion: %s", SUG_C03_01)
        Display("- No Password  Minlen set...", "WARNING")
    elif t_minlen <= '7': # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_01: %s", WRN_C03_01)
        logger.warning("Suggestion: %s", SUG_C03_01)
        Display("- Wrong Password  Minlen set...", "WARNING")
    else:
        logger.info("Has Password Minlen set, checking OK")
        Display("- Has Password  Minlen set...", "OK")


    InsertSection("check passwd minclass set")
    # ------------------------------------------------------------------------------------------------
    if t_minclass == '':
        Display("- No Password  Minclass set...", "WARNING")
    elif t_minlen < '2': # should >= 2
        Display("- Wrong Password  Minclass set...", "WARNING")
    else:
        logger.info("Has Password Minclass set, checking OK")
        Display("- Has Password  Minclass set...", "OK")



    InsertSection("check passwd ucredit set")
    # ------------------------------------------------------------------------------------------------
    if n_ucredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_04: %s", WRN_C03_04)
        logger.warning("Suggestion: %s", SUG_C03_02)
        Display("- No Password  ucredit set...", "WARNING")
    elif n_ucredit > '-1': # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_03: %s", WRN_C03_03)
        logger.warning("Suggestion: %s", SUG_C03_02)
        Display("- Wrong Password  ucredit set...", "WARNING")
    else:
        logger.info("Has Password ucredit set, checking OK")
        Display("- Has Password  ucredit set...", "OK")


    InsertSection("check passwd lcredit set")
    # ------------------------------------------------------------------------------------------------
    if n_lcredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_06: %s", WRN_C03_06)
        logger.warning("Suggestion: %s", SUG_C03_03)
        Display("- No Password  lcredit set...", "WARNING")
    elif n_lcredit > '-1': # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_05: %s", WRN_C03_05)
        logger.warning("Suggestion: %s", SUG_C03_03)
        Display("- Wrong Password  lcredit set...", "WARNING")
    else:
        logger.info("Has Password lcredit set, checking OK")
        Display("- Has Password  lcredit set...", "OK")


    InsertSection("check passwd dcredit set")
    # ------------------------------------------------------------------------------------------------
    if n_dcredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_08: %s", WRN_C03_08)
        logger.warning("Suggestion: %s", SUG_C03_04)
        Display("- No Password  dcredit set...", "WARNING")
    elif n_dcredit > '-1': # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_07: %s", WRN_C03_07)
        logger.warning("Suggestion: %s", SUG_C03_04)
        Display("- Wrong Password  dcredit set...", "WARNING")
    else:
        logger.info("Has Password dcredit set, checking OK")
        Display("- Has Password  dcredit set...", "OK")


    InsertSection("check passwd ocredit set")
    # ------------------------------------------------------------------------------------------------
    if n_ocredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_10: %s", WRN_C03_10)
        logger.warning("Suggestion: %s", SUG_C03_05)
        Display("- No Password  ocredit set...", "WARNING")
    elif n_ocredit > '-1': # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_09: %s", WRN_C03_09)
        logger.warning("Suggestion: %s", SUG_C03_05)
        Display("- Wrong Password  ocredit set...", "WARNING")
    else:
        logger.info("Has Password ocredit set, checking OK")
        Display("- Has Password  ocredit set...", "OK")
