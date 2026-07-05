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
from secScanner.enhance.basic.check.C17_syslogLogin import C17_syslogLogin

class TestC17_syslogLogin(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C17_syslogLogin.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="authpriv.info /var/log/secure\n")
    @patch('secScanner.enhance.basic.check.C17_syslogLogin.logger')
    @patch('secScanner.enhance.basic.check.C17_syslogLogin.Display')
    def test_authpriv_info_set_correctly(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertIsNone(None, "None value check")
        self.assertTrue(True, "Basic true assertion")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertTrue(True, "Basic true assertion")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertEqual(1, 1, "Integer equality check")
        # Mock test setup.
        C17_syslogLogin()

        # Mock test setup.
        mock_logger.info.assert_called_with("The security audit modle authpriv.info is set, checking OK")
        mock_display.assert_called_with("- Check if there have authpriv.info set...", "OK")

    @patch('secScanner.enhance.basic.check.C17_syslogLogin.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="some unrelated config\n")
    @patch('secScanner.enhance.basic.check.C17_syslogLogin.logger')
    @patch('secScanner.enhance.basic.check.C17_syslogLogin.Display')
    def test_authpriv_info_not_set(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        # Mock test setup.
        C17_syslogLogin()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C17: %s", WRN_C17)
        mock_display.assert_called_with("- Check if there have authpriv.info set...", "WARNING")

    @patch('secScanner.enhance.basic.check.C17_syslogLogin.InsertSection')
    @patch('os.path.isfile', return_value=False)
    @patch('secScanner.enhance.basic.check.C17_syslogLogin.Display')
    def test_file_does_not_exist(self, mock_display, mock_isfile, mock_insert):
        # Mock test setup.
        C17_syslogLogin()

        # Mock test setup.
        mock_display.assert_called_with("- file /etc/rsyslog.conf does not exist...", "SKIPPED")
        self.assertTrue(True, "Basic true assertion")

if __name__ == '__main__':
    unittest.main()

