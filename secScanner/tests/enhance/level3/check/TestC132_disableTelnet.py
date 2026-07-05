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
import secScanner
from secScanner.enhance.level3.check.C132_disableTelnet import C132_disableTelnet  # Mock test setup.
from secScanner.lib.textInfo_level3 import *
from secScanner.lib.textInfo_basic import *


class TestC132_disableTelnet(unittest.TestCase):
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.Display')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.logger')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.InsertSection')
    def test_telnet_disabled(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        # Mock test setup.
        C132_disableTelnet()

        mock_InsertSection.assert_called_once_with("Check if telnet is not enabled")
        # Mock test setup.
        mock_display.assert_called_once_with("- Telnet not enabled...", "OK")
        # Mock test setup.
        mock_logger.info.assert_called_once_with("Telnet not enabled...")
        # Mock test setup.
        mock_file.assert_not_called()  # Mock test setup.

    @patch('subprocess.getstatusoutput', return_value=(0, ''))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.Display')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.logger')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.InsertSection')
    def test_telnet_enabled(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        # Mock test setup.
        secScanner.enhance.level3.check.C132_disableTelnet.RESULT_FILE = "result_file_path"  # Mock test setup.

        # Mock test setup.
        C132_disableTelnet()

        mock_InsertSection.assert_called_once_with("Check if telnet is not enabled")
        # Mock test setup.
        mock_display.assert_called_once_with("- Telnet enabled...", "WARNING")
        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C132: %s", WRN_C132)
        mock_logger.warning.assert_any_call("SUG_C132: %s", SUG_C132)
        # Mock test setup.
        mock_file.assert_called_once_with("result_file_path", "a")  # Mock test setup.

if __name__ == '__main__':
    unittest.main()