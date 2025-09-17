# -*- coding: utf-8 -*-

'''
   Copyright (c) 2023. China Mobile(SuZhou)Software Technology Co.,Ltd. All rights reserved.
   secScanner is licensed under Mulan PSL v2.
   You can use this software according to the terms and conditions of the Mulan PSL v2.
   You may obtain a copy of Mulan PSL v2 at:
            http://license.coscl.org.cn/MulanPSL2
   THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
   EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
   MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
   See the Mulan PSL v2 for more details.
'''


import os
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0117_prohibitUSBCheck():
    '''
    Function: set the prohibition of USB devices...
    '''
    set_prohibition_usb = seconf.get('euler', 'set_prohibition_usb')
    InsertSection("Set the Prohibition of USB Devices...")
    USB_Flag = 'unset'
    if set_prohibition_usb == 'yes':
        status_value = subprocess.getoutput('modprobe -n -v usb-storage').strip()
        if status_value == 'install /bin/true':
            USB_Flag = 'set'
        else:
            USB_Flag = 'unset'

        if USB_Flag == 'unset':
            ret = subprocess.getstatusoutput('echo "install usb-storage /bin/true" | sudo tee /etc/modprobe.d/prohibit_usb.conf')[0]
            if ret == 0:
                logger.info("Successfully set the Prohibition of USB Devices enable...")
                Display("- Successfully set the Prohibition of USB Devices enable...","FINISHED")
            else:
                logger.error("Failed to set the Prohibition of USB Devices enable...")
                Display("- Failed to set the Prohibition of USB Devices enable...","FAILED")
        else:
            logger.info("The Prohibition of USB Devices is enabled...")
            Display("- The Prohibition of USB Devices is already  enabled...","SKIPPING")
    else:
        Display("- Skip to set the Prohibition of USB Devices now ...","SKIPPING")
