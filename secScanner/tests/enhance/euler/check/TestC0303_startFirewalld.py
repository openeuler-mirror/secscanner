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
from unittest.mock import patch, mock_open
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0303_startFirewalld import C0303_startFirewalld
import secScanner

class TestC0303_startFirewalld(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.InsertSection')
    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.logger')
    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_unexpected_error(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.side_effect = [
            (1, ""),
            (1, ""),
            (1, "")
        ]
        C0303_startFirewalld()
        mock_InsertSection.assert_any_call("Check if firewalld is launched")
        mock_logger.error.assert_any_call("Unexpected error while checking firewalld status")
        mock_display.assert_any_call("- Unexpected error while checking firewalld status...", "FAILED")
    
    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.InsertSection')
    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.logger')
    @patch('secScanner.enhance.euler.check.C0303_startFirewalld.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_only_firewalld_active(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        
        mock_getstatusoutput.side_effect = [
            (0, "active"),
            (3, "inactive"),
            (3, "inactive")
        ]
        C0303_startFirewalld()
        mock_InsertSection.assert_any_call("Check if firewalld is launched")
        mock_logger.info.assert_any_call("Checking Firewalld is active and iptables&nftables is inactive")
        mock_display.assert_any_call("- Checking Firewalld is active", "OK")

if __name__ == '__main__':
    unittest.main()