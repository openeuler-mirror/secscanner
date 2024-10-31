# -*- coding utf-8 -*-

import ctypes
import os
import subprocess
import time
import threading
import logging
from threading import Thread
from secScanner.gconfig import *
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.TextInfo import *

logger = logging.getLogger("secscanner")

DATA_LEN = 4096
READ_WAIT_SECOND = 3
CHECK_WAIT_SECOND = 15
KMODULELIST_TYPE = 0x00800000
sdklib_path = '/usr/lib64/secDetector/libsecDetectorsdk.so'
g_cli_reader = ctypes.c_void_p
g_cli_reader_lock = threading.Lock()

def init_sdklib():
    global secDetectorsdklib
    secDetectorsdklib = ctypes.cdll.LoadLibrary(sdklib_path)
    secDetectorsdklib.secSub.argtypes = [ctypes.c_int]
    secDetectorsdklib.secSub.restype = ctypes.c_void_p
    secDetectorsdklib.secUnsub.argtypes = [ctypes.c_void_p]
    secDetectorsdklib.secUnsub.restype = None
    secDetectorsdklib.secReadFrom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
    secDetectorsdklib.secReadFrom.restype = None

g_module_lsmod = []
g_module_baseline = []

def get_lsmod():
    global g_module_lsmod
    cmd = "lsmod"
    ret, result = subprocess.getstatusoutput(cmd)
    if ret != 0:
        logger.info("R02 chkrootkit kmodule get lsmod error")
        return

    lsmod_list = result.splitlines()
    # remove "Module                  Size  Used by"
    lsmod_list.pop(0)
    for mod in lsmod_list:
        modname = mod.split(" ")
        g_module_lsmod.append(modname[0])

def check_module(data_string: str =""):
    global g_module_baseline
    timeprefix = ""
    if data_string.endswith(", "):
        data_string = data_string[:-2]
    timeprefix, module_list = data_string.split(" event_type=kmodulelist module_name=")
    g_module_baseline = module_list.strip().split(", ")

    get_lsmod()
    module_diff = set(g_module_baseline).difference(set(g_module_lsmod))
    if module_diff:
        logger.info(f"HIDEKMODULE {module_diff}")
    else:
        logger.info("R02 chkrootkit kmodule no hide module")

def thread_func_sub_and_read(num=0):
    global g_cli_reader

    cli_reader = secDetectorsdklib.secSub(KMODULELIST_TYPE)
    g_cli_reader_lock.acquire()
    g_cli_reader = cli_reader
    g_cli_reader_lock.release()

    data = ctypes.create_string_buffer(DATA_LEN)
    data_len = ctypes.c_int(DATA_LEN)
    secDetectorsdklib.secReadFrom(cli_reader, data, data_len)

    data_string = ""
    check_module_flag = 0
    while True:
        if data_string == 'end':
            break
        ret = data_string.find("event_type=kmodulelist")
        if ret != -1:
            check_module_flag = 1
            break
        time.sleep(READ_WAIT_SECOND)
        secDetectorsdklib.secReadFrom(cli_reader, data, data_len)
        data_string = data.value.decode()

    if check_module_flag == 1:
        check_module(data_string)
    logger.info("R02 chkrootkit kmodule read success")

def thread_func_unsub(num=0):
    global g_cli_reader
    g_cli_reader_lock.acquire()
    try:
        secDetectorsdklib.secUnsub(g_cli_reader)
    finally:
        g_cli_reader_lock.release()
    logger.info("R02 chkrootkit kmodule unsub")

def R02_chkrootkit_kmodule():
    if not os.path.exists(sdklib_path):
        logger.info("the system doesn't install secDetector, please install it ...")
        Display("- No secDetector install...", "WARNING")
        return
    init_sdklib()
    threadlist = []

    tsub_read = Thread(target=thread_func_sub_and_read,args=(1,))
    tsub_read.start()

    time.sleep(CHECK_WAIT_SECOND)
    tunsub = Thread(target=thread_func_unsub,args=(2,))
    tunsub.start()

    threadlist.append(tsub_read)
    threadlist.append(tunsub)

    for t in threadlist:
        t.join()

