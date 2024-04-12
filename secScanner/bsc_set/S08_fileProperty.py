import os,stat
import re
import sys
from secScanner.lib import *
from secScanner.gconfig import *
import logging
import pathlib
import shutil
    
logger = logging.getLogger("secscanner")


def S08_fileProperty():
    InsertSection("Set the file property...")
    SET_FILE_PROPERTY = seconf.get('basic', 'set_file_property')
    BASIC_OPTIONS = seconf.options('basic')  # search basic and show all options
    CHMOD_644_FILE = []
    CHMOD_600_FILE = []
    CHMOD_400_FILE = []
    CHMOD_750_FILE = []
    CHMOD_751_FILE = []
    CHMOD_700_FILE = []
    CHMOD_GWX_FILE = []
    if 'chmod_644_file' in BASIC_OPTIONS:  # if there is a 'chmod 644 file', save the value in a list
        CHMOD_644_FILE = seconf.get('basic', 'chmod_644_file').split()
    if 'chmod_750_file' in BASIC_OPTIONS:
        CHMOD_750_FILE = seconf.get('basic', 'chmod_750_file').split()
    if 'chmod_600_file' in BASIC_OPTIONS:
        CHMOD_600_FILE = seconf.get('basic', 'chmod_600_file').split()
    if 'chmod_400_file' in BASIC_OPTIONS:
        CHMOD_400_FILE = seconf.get('basic', 'chmod_400_file').split()
    if 'chmod_751_file' in BASIC_OPTIONS:
        CHMOD_751_FILE = seconf.get('basic', 'chmod_751_file').split()
    if 'chmod_700_file' in BASIC_OPTIONS:
        CHMOD_700_FILE = seconf.get('basic', 'chmod_700_file').split()
    if 'chmod_gwx_file' in BASIC_OPTIONS:
        gwx_dir = seconf.get('basic', 'chmod_gwx_file').split()
        pathdir = ''.join(gwx_dir)
        gwx_file = os.listdir(pathdir)
        for i in gwx_file:
            CHMOD_GWX_FILE.append(pathdir+i)
    if SET_FILE_PROPERTY == 'yes':
        record_file = '/etc/secscanner.d/fdproperty_record'
        if not os.path.exists(record_file):
            pathlib.Path(record_file).touch()
        if not os.path.getsize(record_file):
            with open(record_file, 'w') as f:
                if CHMOD_644_FILE:
                    for i in CHMOD_644_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_750_FILE:
                    for i in CHMOD_750_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_600_FILE:
                    for i in CHMOD_600_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_400_FILE:
                    for i in CHMOD_400_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_751_FILE:
                    for i in CHMOD_751_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_700_FILE:
                    for i in CHMOD_700_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
                if CHMOD_GWX_FILE:
                    for i in CHMOD_GWX_FILE:
                        if os.path.exists(i):
                            file_permission = oct(os.stat(i).st_mode)[-3:]  # get the property
                            f.write(f"{i}={file_permission}\n")
        ##chmod file and dir
        if CHMOD_644_FILE:
            for i in CHMOD_644_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o644)
        if CHMOD_750_FILE:
            for i in CHMOD_750_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o750)
        if CHMOD_600_FILE:
            for i in CHMOD_600_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o600)
        if CHMOD_400_FILE:
            for i in CHMOD_400_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o400)
        if CHMOD_751_FILE:
            for i in CHMOD_751_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o751)
        if CHMOD_700_FILE:
            for i in CHMOD_700_FILE:
                if os.path.exists(i):
                    os.chmod(i, 0o700)
        if CHMOD_GWX_FILE:
            for i in CHMOD_GWX_FILE:
                if os.path.exists(i):
                    ret, result = subprocess.getstatusoutput(f'chmod go-wx {i}')
                    if ret != 0:
                        logger.warning('Command execution failed')
                        Display("- Command execution failed...", "FAILED")
                        sys.exit(1)
        logger.info("Set the file property finished")
        Display("- Set the file property...", "FINISHED")
    else:
        Display("- Skip set security file property due to config file...", "SKIPPING")
