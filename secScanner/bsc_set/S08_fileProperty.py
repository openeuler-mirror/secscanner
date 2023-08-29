import os
import re
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import pathlib
def S08_fileProperty():
    InsertSection("Set the file property...")
    logger = logging.getLogger("secscanner")
    SET_FILE_PROPERTY = seconf.get('basic', 'set_file_property')
    BASIC_OPTIONS = seconf.options('basic')#search basic and show all options
    CHMOD_644_FILE = []
    CHMOD_600_FILE = []
    CHMOD_400_FILE = []
    CHMOD_750_FILE = [] # declare variable just in case
    if ('chmod_644_file' in BASIC_OPTIONS):# if there is a 'chmod 644 file', save the value in a list
        CHMOD_644_FILE = seconf.get('basic', 'chmod_644_file').split()
    if ('chmod_750_file' in BASIC_OPTIONS):
        CHMOD_750_FILE = seconf.get('basic', 'chmod_750_file').split()
    if ('chmod_600_file' in BASIC_OPTIONS):
        CHMOD_600_FILE = seconf.get('basic', 'chmod_600_file').split()
    if ('chmod_400_file' in BASIC_OPTIONS):
        CHMOD_400_FILE = seconf.get('basic', 'chmod_400_file').split()
    if ('chmod_751_file' in BASIC_OPTIONS):
        CHMOD_751_FILE = seconf.get('basic', 'chmod_751_file').split()
    if SET_FILE_PROPERTY == 'yes':
        pathlib.Path('/etc/bse.d/fdproperty_record').touch()
        PRO_RECORD_DIR = '/etc/bse.d/fdproperty_record'
        if not (os.path.exists(PRO_RECORD_DIR) and os.path.getsize(PRO_RECORD_DIR)):
            if CHMOD_644_FILE != []:
                for i in CHMOD_644_FILE:
                    if os.path.exists(i):
                        file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                        with open(PRO_RECORD_DIR, 'a') as add_file:
                            add_file.write(f"{i}={file_permission}\n")
            if CHMOD_750_FILE != []:
                for i in CHMOD_750_FILE:
                    if os.path.exists(i):
                        file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                        with open(PRO_RECORD_DIR, 'a') as add_file:
                            add_file.write(f"{i}={file_permission}\n")
            if CHMOD_600_FILE != []:
                for i in CHMOD_600_FILE:
                    if os.path.exists(i):
                        file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                        with open(PRO_RECORD_DIR, 'a') as add_file:
                            add_file.write(f"{i}={file_permission}\n")
            if CHMOD_400_FILE != []:
                for i in CHMOD_400_FILE:
                    if os.path.exists(i):
                        file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                        with open(PRO_RECORD_DIR, 'a') as add_file:
                            add_file.write(f"{i}={file_permission}\n")
            if CHMOD_751_FILE != []:
                for i in CHMOD_751_FILE:
                    if os.path.exists(i):
                        file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                        with open(PRO_RECORD_DIR, 'a') as add_file:
                            add_file.write(f"{i}={file_permission}\n")

##chmod file and dir
        if CHMOD_644_FILE != []:
            for i in CHMOD_644_FILE:
                if os.path.exists(i):
                    os.chmod(i, 644)
        if CHMOD_750_FILE != []:
            for i in CHMOD_750_FILE:
                if os.path.exists(i):
                    os.chmod(i, 750)
        if CHMOD_600_FILE != []:
            for i in CHMOD_600_FILE:
                if os.path.exists(i):
                    os.chmod(i, 600)
        if CHMOD_400_FILE != []:
            for i in CHMOD_400_FILE:
                if os.path.exists(i):
                    os.chmod(i, 400)
        if CHMOD_751_FILE != []:
            for i in CHMOD_751_FILE:
                if os.path.exists(i):
                    os.chmod(i, 751)
        logger.info("Set the file property finished")
        Display(f"- Set the file property...", "FINISHED")
    else:
        Display(f"- Skip set security file property due to config file...", "SKIPPING")