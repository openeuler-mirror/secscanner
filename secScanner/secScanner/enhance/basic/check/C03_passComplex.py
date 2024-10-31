import logging
import re
from secScanner.gconfig import *
from secScanner.lib import *

logger = logging.getLogger("secscanner")

def C03_passComplex():
    InsertSection("check password complexity set")
    # only one minlen minclass ...count don't need
    regex_minlen = r'(?<=minlen=).[0-9]*'
    regex_minclass = r'(?<=minclass=).[0-9]*'
    regex_ucredit = r'(?<=ucredit=).[0-9]*'
    regex_lcredit = r'(?<=lcredit=).[0-9]*'
    regex_dcredit = r'(?<=dcredit=).[0-9]*'
    regex_ocredit = r'(?<=ocredit=).[0-9]*'
    t_minlen = ''  # if not match minlen, t_minlen= ''
    t_minclass = ''
    n_ucredit = ''
    n_lcredit = ''
    n_dcredit = ''
    n_ocredit = ''

    # search part
    with open("/etc/pam.d/system-auth", "r") as file:
        lines = file.readlines()
        for line in lines:
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('minlen=', line):
                temp = re.findall(regex_minlen, line)
                if temp != []:
                    t_minlen = temp[0]  # must found num,  if temp == [] means no number after "minlen" No password set
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('minclass=', line):
                temp = re.findall(regex_minclass, line)
                if temp != []:
                    t_minclass = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('ucredit=', line):
                temp = re.findall(regex_ucredit, line)
                if temp != []:
                    n_ucredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('lcredit=', line):
                temp = re.findall(regex_lcredit, line)
                if temp != []:
                    n_lcredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('dcredit=', line):
                temp = re.findall(regex_dcredit, line)
                if temp != []:
                    n_dcredit = temp[0]
            if re.match('password', line) and re.search('pam_pwquality.so', line) and re.search('ocredit=', line):
                temp = re.findall(regex_ocredit, line)
                if temp != []:
                    n_ocredit = temp[0]

    # decide part
    # ------------------------------------------------------------------------------------------------
    if t_minlen == '':
        # minlen not found or no numbers after minlen
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_02: %s", WRN_C03_02)
        logger.warning("SUG_C03_01: %s", SUG_C03_01)
        Display("- No Password Minlen set...", "WARNING")
    elif t_minlen <= '7':  # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_01: %s", WRN_C03_01)
        logger.warning("SUG_C03_01: %s", SUG_C03_01)
        Display("- Wrong Password Minlen set...", "WARNING")
    else:
        logger.info("Has Password Minlen set, checking OK")
        Display("- Has Password Minlen set...", "OK")

    # ------------------------------------------------------------------------------------------------
    if t_minclass == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_04: %s", WRN_C03_04)
        logger.warning("SUG_C03_02: %s", SUG_C03_02)
        Display("- No Password Minclass set...", "WARNING")
    elif t_minclass < '2':  # should >= 2
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_03: %s", WRN_C03_03)
        logger.warning("SUG_C03_02: %s", SUG_C03_02)
        Display("- Wrong Password Minclass set...", "WARNING")
    else:
        logger.info("Has Password Minclass set, checking OK")
        Display("- Has Password Minclass set...", "OK")

    # ------------------------------------------------------------------------------------------------
    if n_ucredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_06: %s", WRN_C03_06)
        logger.warning("SUG_C03_03: %s", SUG_C03_03)
        Display("- No Password ucredit set...", "WARNING")
    elif n_ucredit > '-1':  # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_05: %s", WRN_C03_05)
        logger.warning("SUG_C03_03: %s", SUG_C03_03)
        Display("- Wrong Password ucredit set...", "WARNING")
    else:
        logger.info("Has Password ucredit set, checking OK")
        Display("- Has Password ucredit set...", "OK")

    # ------------------------------------------------------------------------------------------------
    if n_lcredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_08: %s", WRN_C03_08)
        logger.warning("SUG_C03_04: %s", SUG_C03_04)
        Display("- No Password lcredit set...", "WARNING")
    elif n_lcredit > '-1':  # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_07: %s", WRN_C03_07)
        logger.warning("SUG_C03_04: %s", SUG_C03_04)
        Display("- Wrong Password lcredit set...", "WARNING")
    else:
        logger.info("Has Password lcredit set, checking OK")
        Display("- Has Password lcredit set...", "OK")

    # ------------------------------------------------------------------------------------------------
    if n_dcredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_10: %s", WRN_C03_10)
        logger.warning("SUG_C03_05: %s", SUG_C03_05)
        Display("- No Password dcredit set...", "WARNING")
    elif n_dcredit > '-1':  # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_09: %s", WRN_C03_09)
        logger.warning("SUG_C03_05: %s", SUG_C03_05)
        Display("- Wrong Password dcredit set...", "WARNING")
    else:
        logger.info("Has Password dcredit set, checking OK")
        Display("- Has Password dcredit set...", "OK")

    # ------------------------------------------------------------------------------------------------
    if n_ocredit == '':
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_12: %s", WRN_C03_12)
        logger.warning("SUG_C03_06: %s", SUG_C03_06)
        Display("- No Password ocredit set...", "WARNING")
    elif n_ocredit > '-1':  # '' < '7' but '' cant enter here
        with open(RESULT_FILE, "a") as file:
            file.write("\nC03\n")
        logger.warning("WRN_C03_11: %s", WRN_C03_11)
        logger.warning("SUG_C03_06: %s", SUG_C03_06)
        Display("- Wrong Password ocredit set...", "WARNING")
    else:
        logger.info("Has Password ocredit set, checking OK")
        Display("- Has Password ocredit set...", "OK")
