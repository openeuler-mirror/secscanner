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


import unittest
from unittest.mock import patch, MagicMock
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0122_checkSoftwareInstall import C0122_checkSoftwareInstall  # Replace with actual module path
import logging

class TestC0122_CheckSoftwareInstall(unittest.TestCase):

    @patch('subprocess.getstatusoutput')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.logger')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.Display')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.InsertSection')
    def test_ftp_installed(self, mock_InsertSection, mock_Display, mock_logger, mock_open, mock_getstatusoutput):
        # Mock the subprocess.getstatusoutput to return FTP installed status
        mock_getstatusoutput.side_effect = [
            (0, 'package ftp is installed'),
            (1, 'package tftp is not installed'),
            (1, 'package telnet is not installed'),
            (1, 'package net-snmp is not installed'),
            (1, 'package python2 is not installed'),
        ]

        # Execute the function
        C0122_checkSoftwareInstall()

        # Validate FTP installed
        mock_open().write.assert_any_call("\nC0122_1\n")
        mock_logger.warning.assert_any_call("WRN_C0122_1: %s", WRN_C0122_1)
        mock_logger.warning.assert_any_call("SUG_C0122_1: %s", SUG_C0122_1)
        mock_Display.assert_any_call("- Check the  FTP software is installed...", "WARNING")

    @patch('subprocess.getstatusoutput')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.logger')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.Display')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.InsertSection')
    def test_tftp_installed(self, mock_InsertSection, mock_Display, mock_logger, mock_open, mock_getstatusoutput):
        # Mock the subprocess.getstatusoutput to return TFTP installed status
        mock_getstatusoutput.side_effect = [
            (1, 'package ftp is not installed'),
            (0, 'package tftp is installed'),
            (1, 'package telnet is not installed'),
            (1, 'package net-snmp is not installed'),
            (1, 'package python2 is not installed'),
        ]

        # Execute the function
        C0122_checkSoftwareInstall()

        # Validate TFTP installed
        mock_open().write.assert_any_call("\nC0122_2\n")
        mock_logger.warning.assert_any_call("WRN_C0122_2: %s", WRN_C0122_2)
        mock_logger.warning.assert_any_call("SUG_C0122_2: %s", SUG_C0122_2)
        mock_Display.assert_any_call("- Check the TFTP software is installed...", "WARNING")
    
    @patch('subprocess.getstatusoutput')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.logger')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.Display')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.InsertSection')
    def test_telnet_installed(self, mock_InsertSection, mock_Display, mock_logger, mock_open, mock_getstatusoutput):
        # Mock the subprocess.getstatusoutput to return Telnet installed status
        mock_getstatusoutput.side_effect = [
            (1, 'package ftp is not installed'),
            (1, 'package tftp is not installed'),
            (0, 'package telnet is installed'),
            (1, 'package net-snmp is not installed'),
            (1, 'package python2 is not installed'),
        ]

        # Execute the function
        C0122_checkSoftwareInstall()

        # Validate Telnet installed
        mock_open().write.assert_any_call("\nC0122_3\n")
        mock_logger.warning.assert_any_call("WRN_C0122_3: %s", WRN_C0122_3)
        mock_logger.warning.assert_any_call("SUG_C0122_3: %s", SUG_C0122_3)
        mock_Display.assert_any_call("- Check the Telnet software is installed...", "WARNING")

    @patch('subprocess.getstatusoutput')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.logger')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.Display')
    @patch('secScanner.enhance.euler.check.C0122_checkSoftwareInstall.InsertSection')
    def test_net_snmp_installed(self, mock_InsertSection, mock_Display, mock_logger, mock_open, mock_getstatusoutput):
        # Mock the subprocess.getstatusoutput to return Net-snmp installed status
        mock_getstatusoutput.side_effect = [
            (1, 'package ftp is not installed'),
            (1, 'package tftp is not installed'),
            (1, 'package telnet is not installed'),
            (0, 'package net-snmp is installed'),
            (1, 'package python2 is not installed'),
        ]

        # Execute the function
        C0122_checkSoftwareInstall()

        # Validate Net-snmp installed
        mock_open().write.assert_any_call("\nC0122_4\n")
        mock_logger.warning.assert_any_call("WRN_C0122_4: %s", WRN_C0122_4)
        mock_logger.warning.assert_any_call("SUG_C0122_4: %s", SUG_C0122_4)
        mock_Display.assert_any_call("- Check the Net-snmpsoftware is installed...", "WARNING")
if __name__ == '__main__':
    unittest.main()