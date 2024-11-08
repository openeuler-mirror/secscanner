# -*- coding: utf-8 -*-

import logging
import subprocess
from secScanner.gconfig import *
from secScanner.lib import *
logger = logging.getLogger("secscanner")

def C0122_checkSoftwareInstall():
    '''
    Function: Check the Ftp installed 
    '''
    InsertSection("Check whether the FTP software is installed in your Linux System ")
    ret,res = subprocess.getstatusoutput('rpm -q ftp')
    if ret == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0122_1\n")
        logger.warning("WRN_C0122_1: %s", WRN_C0122_1)
        logger.warning("SUG_C0122_1: %s", SUG_C0122_1)
        Display(f"- Check the  FTP software is installed...", "WARNING")
    else:
        logger.info(f"The Ftp status is: {res}")
        Display(f"- Check the FTP software is uninstall...", "OK")
    
    '''
    Function: Check the TFtp installed 
    '''
    InsertSection("Check whether the TFTP software is installed in your Linux System ")
    ret2,res2 = subprocess.getstatusoutput('rpm -q tftp')
    if ret2 == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0122_2\n")
        logger.warning("WRN_C0122_2: %s", WRN_C0122_2)
        logger.warning("SUG_C0122_2: %s", SUG_C0122_2)
        Display(f"- Check the TFTP software is installed...", "WARNING")
    else:
        logger.info(f"The TFTP status is: {res2}")
        Display(f"- Check the TFTP software is uninstall...", "OK")
    
    '''
    Function: Check the Telnet installed 
    '''
    InsertSection("Check whether the Telnet software is installed in your Linux System ")
    ret3,res3 = subprocess.getstatusoutput('rpm -q telnet')
    if ret3 == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0122_3\n")
        logger.warning("WRN_C0122_3: %s", WRN_C0122_3)
        logger.warning("SUG_C0122_3: %s", SUG_C0122_3)
        Display(f"- Check the Telnet software is installed...", "WARNING")
    else:
        logger.info(f"The Telnet status is: {res3}")
        Display(f"- Check the Telnet software is uninstall...", "OK")

    '''
    Function: Check the Net-snmp installed 
    '''
    InsertSection("Check whether the Net-snmp software is installed in your Linux System ")
    ret4,res4 = subprocess.getstatusoutput('rpm -q net-snmp')
    if ret4 == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0122_4\n")
        logger.warning("WRN_C0122_4: %s", WRN_C0122_4)
        logger.warning("SUG_C0122_4: %s", SUG_C0122_4)
        Display(f"- Check the Net-snmpsoftware is installed...", "WARNING")
    else:
        logger.info(f"The Net-snmp status is: {res4}")
        Display(f"- Check the Net-snmp software is uninstall...", "OK")

    '''
    Function: Check the Python2 installed 
    '''
    InsertSection("Check whether the Python2 software is installed in your Linux System ")
    ret5,res5 = subprocess.getstatusoutput('rpm -q python2')
    if ret5 == 0:
        with open(RESULT_FILE,'a+') as file:
            file.write("\nC0122_5\n")
        logger.warning("WRN_C0122_5: %s", WRN_C0122_5)
        logger.warning("SUG_C0122_5: %s", SUG_C0122_5)
        Display(f"- Check the Python2 software is installed...", "WARNING")
    else:
        logger.info(f"The Python2 status is: {res5}")
        Display(f"- Check the Python2 software is uninstall...", "OK")