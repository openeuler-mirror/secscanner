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
import logging
import subprocess
from secScanner.lib import *
from secScanner.gconfig import *
logger = logging.getLogger("secscanner")

def S0122_checkSoftwareInstall():
    '''
    Function: Set remove ftp
    '''
    set_remove_ftp = seconf.get('euler', 'set_remove_ftp')
    InsertSection("Remove the Ftp in your Linux System...")
    if set_remove_ftp == 'yes':
        ret,res = subprocess.getstatusoutput('rpm -q ftp')
        if ret != 0:
            Display("- No package for the ftp...", "SKIPPING")
        else:
            try:
                set_result,_= subprocess.getstatusoutput('yum remove -y ftp')
            except Exception:
                os.system('dnf remove ftp')
                
            if set_result == 0:
                logger.info("Set remove the ftp, checking ok")
                Display("- Set remove the ftp...", "FINISHED")
            else:
                logger.warning("Set remove the ftp failed")
                Display("- Set remove the ftp...", "FAILED")
    else:
        Display("- Skip set remove the ftp...", "SKIPPING")
    
    '''
    Function: Set remove tftp
    '''
    set_remove_tftp = seconf.get('euler', 'set_remove_tftp')
    InsertSection("Remove the TFTP in your Linux System...")
    if set_remove_tftp == 'yes':
        ret2,res2 = subprocess.getstatusoutput('rpm -q tftp') 
        if ret2 != 0:
            Display("- No package for tftp...", "SKIPPING")
        else:
            try:
                set_result2,_= subprocess.getstatusoutput('yum remove -y tftp')
            except Exception:
                os.system('dnf remove tftp')
                
            if set_result2 == 0:
                logger.info("Set remove the tftp, checking ok")
                Display("- Set remove the tftp...", "FINISHED")
            else:
                logger.warning("Set remove the tftp failed")
                Display("- Set remove the tftp...", "FAILED")
    else:
        Display("- Skip set remove the tftp...", "SKIPPING")

    '''
    Function: Set remove telnet
    '''
    set_remove_telnet = seconf.get('euler', 'set_remove_telnet')
    InsertSection("Set remove the telnet...")
    if set_remove_telnet == 'yes':
        ret3,res3 = subprocess.getstatusoutput('rpm -q telnet') 
        if ret3 != 0:
            Display("- No package for telnet...", "SKIPPING")
        else:
            try:
                set_result3,_= subprocess.getstatusoutput('yum remove -y telnet')
            except Exception:
                os.system('dnf remove telnet')
                
            if set_result3 == 0:
                logger.info("Set remove the telnet, checking ok")
                Display("- Set remove the telnet...", "FINISHED")
            else:
                logger.warning("Set remove the telnet failed")
                Display("- Set remove the telnet...", "FAILED")
    else:
        Display("- Skip set remove the telnet...", "SKIPPING")
    
    '''
    Function: Set remove net-snmp
    '''
    set_remove_snmp = seconf.get('euler', 'set_remove_snmp')
    InsertSection("Set remove the net-snmp...")
    if set_remove_snmp == 'yes':
        ret4,res4 = subprocess.getstatusoutput('rpm -q net-snmp') 
        if ret4 != 0:
            Display("- No package for net-snmp...", "SKIPPING")
        else:
            try:
                set_result4,_= subprocess.getstatusoutput('yum remove -y net-snmp')
            except Exception:
                os.system('dnf remove net-snmp')
                
            if set_result4 == 0:
                logger.info("Set remove the net-snmp, checking ok")
                Display("- Set remove the net-snmp...", "FINISHED")
            else:
                logger.warning("Set remove the net-snmp failed")
                Display("- Set remove the net-snmp...", "FAILED")
    else:
        Display("- Skip set remove the net-snmp...", "SKIPPING")

    '''
    Function: Set remove python2
    '''
    set_remove_python2 = seconf.get('euler', 'set_remove_python2')
    InsertSection("Set remove the python2...")
    if set_remove_python2 == 'yes':
        ret5,res5 = subprocess.getstatusoutput('rpm -q python2') 
        if ret5 != 0:
            Display("- No package for python2...", "SKIPPING")
        else:
            try:
                set_result5,_= subprocess.getstatusoutput('yum remove -y python2')
            except Exception:
                os.system('dnf remove python2')
            
            if set_result5 == 0:
                logger.info("Set remove the python2, checking ok")
                Display("- Set remove the python2...", "FINISHED")
            else:
                logger.warning("Set remove the python2 failed")
                Display("- Set remove the python2...", "FAILED")
    else:
        Display("- Skip set remove the python2...", "SKIPPING")
