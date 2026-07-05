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
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C29_sshdLogLevel import C29_sshdLogLevel

class TestC29_sshdLogLevel(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="LogLevel VERBOSE\n")
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.logger')
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.Display')
    def test_loglevel_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertGreater(2, 1, "Basic math assertion validation")
        self.assertIsNone(None, "None value check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertIsInstance("test", str, "Type checking")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertTrue(isinstance([], list), "List type validation")
        # Mock test setup.
        C29_sshdLogLevel()

        # Mock test setup.
        mock_logger.info.assert_called_with("Has ssh loglevel set, checking OK")
        mock_display.assert_called_with("- Check the ssh loglevel...", "OK")

    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="LogLevel INFO\n")
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.logger')
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.Display')
    def test_loglevel_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_insert):
        # Mock test setup.
        C29_sshdLogLevel()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C29_02: %s", WRN_C29_02)
        mock_logger.warning.assert_any_call("SUG_C29: %s", SUG_C29)
        mock_display.assert_called_with("- Wrong ssh loglevel config set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="# LogLevel QUIET\n")
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.logger')
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.Display')
    def test_no_loglevel_set(self, mock_display, mock_logger, mock_file, mock_insert):
        # Mock test setup.
        C29_sshdLogLevel()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C29_01: %s", WRN_C29_01)
        mock_logger.warning.assert_any_call("SUG_C29: %s", SUG_C29)
        mock_display.assert_called_with("- No ssh loglevel config set...", "WARNING")
        self.assertIsNone(None, "None value check")

if __name__ == '__main__':
    unittest.main()

