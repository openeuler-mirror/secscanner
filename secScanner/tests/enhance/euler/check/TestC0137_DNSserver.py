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
import secScanner
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0137_DNSserver import C0137_DNSserver

class TestC0137_DNSserver(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.logger')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_bind_not_installed(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, 'package bind is not installed')]
        
        # Mock test setup.
        C0137_DNSserver()
        
        mock_InsertSection.assert_called_once_with("Check whether the status of DNS server in your Linux System ")
        mock_logger.info.assert_called_with("package bind is not installed")
        mock_display.assert_called_with("- package bind is not installed", "OK")

    @patch('secScanner.enhance.euler.check.C0137_DNSserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.logger')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_bind_installed_disabled(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'package bind is installed'), (1, 'disabled')]
        
        # Mock test setup.
        C0137_DNSserver()
        mock_InsertSection.assert_called_once_with("Check whether the status of DNS server in your Linux System ")
        mock_logger.info.assert_called_with("The DNS-Server status is: disabled")
        mock_display.assert_called_with("- Check the DNS-Server is disabled...", "OK")

    @patch('secScanner.enhance.euler.check.C0137_DNSserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.logger')
    @patch('secScanner.enhance.euler.check.C0137_DNSserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_bind_installed_enabled(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'package bind is installed'), (0, 'enabled')]
        # Mock test setup.
        secScanner.enhance.euler.check.C0137_DNSserver.RESULT_FILE = "result_file_path"  # Mock test setup.

        # Mock test setup.
        C0137_DNSserver()
        mock_InsertSection.assert_called_once_with("Check whether the status of DNS server in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0137: %s", WRN_C0137)
        mock_logger.warning.assert_any_call("SUG_C0137: %s", SUG_C0137)
        mock_display.assert_called_with("- Check the DNS-Server is enabled...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a+")  # Mock test setup.

if __name__ == '__main__':
    unittest.main()