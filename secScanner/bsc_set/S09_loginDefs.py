import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import shutil
def S09_loginDefs():
    if not os.path.exists('/etc/login.defs_bak'):
        shutil.copy2('/etc/login.defs', '/etc/login.defs_bak')
    logger = logging.getLogger("secscanner")
    SET_PASS_MAX_DAYS = seconf.get('basic', 'set_pass_max_days')
    PASS_MAX_DAYS_VALUE = seconf.get('basic', 'pass_max_days_value')
    SET_PASS_MIN_DAYS = seconf.get('basic', 'set_pass_min_days')
    PASS_MIN_DAYS_VALUE = seconf.get('basic', 'pass_min_days_value')
    SET_PASS_MIN_LEN = seconf.get('basic', 'set_pass_min_len')
    PASS_MIN_LEN_VALUE = seconf.get('basic', 'pass_min_len_value')
    SET_PASS_WARN_AGE = seconf.get('basic', 'set_pass_warn_age')
    PASS_WARN_AGE_VALUE = seconf.get('basic', 'pass_warn_age_value')

    InsertSection("Set the PASS_MAX_DAYS in /etc/login.defs...")
    if SET_PASS_MAX_DAYS == 'yes':
        IS_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MAX_DAYS', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/login.defs', 'a') as add_file:
                add_file.write(f'\nPASS_MAX_DAYS   {PASS_MAX_DAYS_VALUE}\n')
        else:
            with open('/etc/login.defs', 'w') as write_file:
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('PASS_MAX_DAYS', line):
                        write_file.write(f"PASS_MAX_DAYS   {PASS_MAX_DAYS_VALUE}\n")
                    else:
                        write_file.write(line)
        PASS_RESULT = ''
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MAX_DAYS', line):
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1].isdigit():
                        PASS_RESULT = temp[1]
        if PASS_RESULT > '90':
            logger.info("the PASS_MAX_DAYS is not safe")
            Display("- Set the PASS_MAX_DAYS value...", "FAILED")
        else:
            logger.info("the PASS_MAX_DAYS is safe, checking ok")
            Display("- Set the PASS_MAX_DAYS value...", "FINISHED")
    else:
        Display("- Skip set PASS_MAX_DAYS due to config file...", "SKIPPING")

    InsertSection("Set the PASS_MIN_DAYS in /etc/login.defs...")
    if SET_PASS_MIN_DAYS == 'yes':
        IS_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MIN_DAYS', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/login.defs', 'a') as add_file:
                add_file.write(f'\nPASS_MIN_DAYS   {PASS_MIN_DAYS_VALUE}\n')
        else:
            with open('/etc/login.defs', 'w') as write_file:
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('PASS_MIN_DAYS', line):
                        write_file.write(f"PASS_MIN_DAYS   {PASS_MIN_DAYS_VALUE}\n")
                    else:
                        write_file.write(line)
        PASS_RESULT = ''
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MIN_DAYS', line):
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1].isdigit():
                        PASS_RESULT = temp[1]
        if PASS_RESULT < '6':
            logger.info("the PASS_MIN_DAYS is not safe")
            Display("- Set the PASS_MIN_DAYS value...", "FAILED")
        else:
            logger.info("the PASS_MIN_DAYS is safe, checking ok")
            Display("- Set the PASS_MIN_DAYS value...", "FINISHED")
    else:
        Display("- Skip set PASS_MIN_DAYS due to config file...", "SKIPPING")

    InsertSection("Set the PASS_MIN_LEN in /etc/login.defs...")
    if SET_PASS_MIN_LEN == 'yes':
        IS_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MIN_LEN', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/login.defs', 'a') as add_file:
                add_file.write(f'\nPASS_MIN_LEN   {PASS_MIN_LEN_VALUE}\n')
        else:
            with open('/etc/login.defs', 'w') as write_file:
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('PASS_MIN_LEN', line):
                        write_file.write(f"PASS_MIN_LEN   {PASS_MIN_LEN_VALUE}\n")
                    else:
                        write_file.write(line)
        PASS_RESULT = ''
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_MIN_LEN', line):
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1].isdigit():
                        PASS_RESULT = temp[1]
        if PASS_RESULT < '8':
            logger.info("the PASS_MIN_LEN is not safe")
            Display("- Set the PASS_MIN_LEN value...", "FAILED")
        else:
            logger.info("the PASS_MIN_LEN is safe, checking ok")
            Display("- Set the PASS_MIN_LEN value...", "FINISHED")
    else:
        Display("- Skip set PASS_MIN_LEN due to config file...", "SKIPPING")

    InsertSection("Set the PASS_WARN_AGE in /etc/login.defs...")
    if SET_PASS_WARN_AGE == 'yes':
        IS_EXIST = 0
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_WARN_AGE', line):
                    IS_EXIST = 1
        if IS_EXIST == 0:
            with open('/etc/login.defs', 'a') as add_file:
                add_file.write(f'\nPASS_WARN_AGE   {PASS_WARN_AGE_VALUE}\n')
        else:
            with open('/etc/login.defs', 'w') as write_file:
                for line in lines:
                    if (not re.match('#|$', line)) and re.search('PASS_WARN_AGE', line):
                        write_file.write(f"PASS_WARN_AGE   {PASS_WARN_AGE_VALUE}\n")
                    else:
                        write_file.write(line)
        PASS_RESULT = ''
        with open('/etc/login.defs', 'r') as read_file:
            lines = read_file.readlines()
            for line in lines:
                if (not re.match('#|$', line)) and re.search('PASS_WARN_AGE', line):
                    temp = line.strip('\n').split()
                    if len(temp) == 2 and temp[1].isdigit():
                        PASS_RESULT = temp[1]
        if PASS_RESULT < '30':
            logger.info("the PASS_WARN_AGE is not safe")
            Display("- Set the PASS_WARN_AGE value...", "FAILED")
        else:
            logger.info("the PASS_WARN_AGE is safe, checking ok")
            Display("- Set the PASS_WARN_AGE value...", "FINISHED")
    else:
        Display("- Skip set PASS_WARN_AGE due to config file...", "SKIPPING")
