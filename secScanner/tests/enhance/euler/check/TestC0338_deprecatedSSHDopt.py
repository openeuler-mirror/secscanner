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
from secScanner.enhance.euler.check.C0338_deprecatedSSHDopt import C0338_deprecatedSSHDopt
import secScanner


class TestC0338_deprecatedSSHDopt(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.InsertSection')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.logger')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_cmd_fail(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (1, "")
        secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.RESULT_FILE = "result_file_path"  # Mock test setup.
        C0338_deprecatedSSHDopt()
        mock_InsertSection.assert_any_call("Check deprecated sshd options in sshd config file")
        mock_logger.warning.assert_any_call("WRN_C0338_02: %s", WRN_C0338_02)
        mock_logger.warning.assert_any_call("SUG_C0338_02: %s", SUG_C0338_02)
        mock_display.assert_any_call("- Error occured while excute sshd -t command...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.InsertSection')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.logger')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_not_found(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (0, "")
        C0338_deprecatedSSHDopt()
        mock_InsertSection.assert_any_call("Check deprecated sshd options in sshd config file")
        mock_logger.info.assert_any_call("Check found 0 deprecated option of sshd")
        mock_display.assert_any_call("- Check found 0 deprecated option of sshd", "OK")
        
    
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.InsertSection')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.logger')
    @patch('secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_found_success(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection):
        mock_getstatusoutput.return_value = (0, "Deprecated option")
        secScanner.enhance.euler.check.C0338_deprecatedSSHDopt.RESULT_FILE = "result_file_path"  # Mock test setup.
        C0338_deprecatedSSHDopt()
        mock_InsertSection.assert_any_call("Check deprecated sshd options in sshd config file")
        mock_logger.warning.assert_any_call("WRN_C0338_01: %s", WRN_C0338_01)
        mock_logger.warning.assert_any_call("SUG_C0338_01: %s", SUG_C0338_01)
        mock_display.assert_any_call("- Found deprecated option of sshd...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()