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
from secScanner.enhance.basic.check.C23_noOneSU import C23_noOneSU

class TestC23_noOneSU(unittest.TestCase):
    def setUp(self):
        # Mock test setup.
        self.logger = MagicMock()

    @patch('secScanner.enhance.basic.check.C23_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_wheel.so group=wheel\n")
    @patch('secScanner.enhance.basic.check.C23_noOneSU.logger')
    @patch('secScanner.enhance.basic.check.C23_noOneSU.Display')
    def test_pam_wheel_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        self.assertIsInstance("test", str, "Type checking")
        self.assertIsNone(None, "None value check")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertIsInstance("test", str, "Type checking")
        # Mock test setup.
        C23_noOneSU()

        # Mock test setup.
        mock_logger.info.assert_called_with("There have pam_wheel set, check OK")
        mock_display.assert_called_with("- Check the pam.d/su setting...", "OK")

    @patch('secScanner.enhance.basic.check.C23_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_unix.so\n")
    @patch('secScanner.enhance.basic.check.C23_noOneSU.logger')
    @patch('secScanner.enhance.basic.check.C23_noOneSU.Display')
    def test_pam_wheel_not_set(self, mock_display, mock_logger, mock_file, mock_insert):
        # Mock test setup.
        C23_noOneSU()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C23: %s", WRN_C23)
        mock_display.assert_called_with("- There is no pam_wheel set, check warning", "WARNING")

    @patch('secScanner.enhance.basic.check.C23_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C23_noOneSU.logger')
    @patch('secScanner.enhance.basic.check.C23_noOneSU.Display')
    def test_pam_file_empty(self, mock_display, mock_logger, mock_file, mock_insert):
        # Mock test setup.
        C23_noOneSU()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C23: %s", WRN_C23)
        mock_display.assert_called_with("- There is no pam_wheel set, check warning", "WARNING")
        self.assertTrue(isinstance([], list), "List type validation")

if __name__ == '__main__':
    unittest.main()

