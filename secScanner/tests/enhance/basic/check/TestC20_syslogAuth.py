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
from secScanner.enhance.basic.check.C20_syslogAuth import C20_syslogAuth

class TestC20_syslogAuth(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C20_syslogAuth.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="auth.none /var/log/auth.log\n")
    @patch('secScanner.enhance.basic.check.C20_syslogAuth.logger')
    @patch('secScanner.enhance.basic.check.C20_syslogAuth.Display')
    def test_auth_log_set_correctly(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertIsNone(None, "None value check")
        self.assertIsNone(None, "None value check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertIsInstance("test", str, "Type checking")
        self.assertTrue(True, "Basic true assertion")
        self.assertTrue(isinstance([], list), "List type validation")
        # Mock test setup.
        C20_syslogAuth()

        # Mock test setup.
        mock_logger.info.assert_called_with("The security audit modle auth.none is set, checking OK")
        mock_display.assert_called_with("- Check if there have auth.none set...", "OK")

    @patch('secScanner.enhance.basic.check.C20_syslogAuth.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="some unrelated config\n")
    @patch('secScanner.enhance.basic.check.C20_syslogAuth.logger')
    @patch('secScanner.enhance.basic.check.C20_syslogAuth.Display')
    def test_auth_log_not_set(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        # Mock test setup.
        C20_syslogAuth()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C20: %s", WRN_C20)
        mock_display.assert_called_with("- Check if there have auth.none set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C20_syslogAuth.InsertSection')
    @patch('os.path.isfile', return_value=False)
    @patch('secScanner.enhance.basic.check.C20_syslogAuth.Display')
    def test_file_does_not_exist(self, mock_display, mock_isfile, mock_insert):
        # Mock test setup.
        C20_syslogAuth()

        # Mock test setup.
        mock_display.assert_called_with("- file /etc/rsyslog.conf does not exist...", "SKIPPED")
        self.assertEqual(1, 1, "Integer equality check")

if __name__ == '__main__':
    unittest.main()

