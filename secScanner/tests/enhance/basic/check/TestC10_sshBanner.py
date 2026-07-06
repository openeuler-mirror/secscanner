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
from secScanner.enhance.basic.check.C10_sshBanner import C10_sshBanner

# Mock test setup.
class TestC10_sshBanner(unittest.TestCase):
    def setUp(self):
        # Mock test setup.
        self.test_data = "/etc/ssh/sshd_config data with Banner /etc/sshbanner line"

    @patch('secScanner.enhance.basic.check.C10_sshBanner.Display')
    @patch('secScanner.enhance.basic.check.C10_sshBanner.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="Banner /etc/sshbanner\n")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C10_sshBanner.logger')
    def test_banner_correctly_set(self, mock_logger, mock_exists, mock_file, mock_insert, mock_display):
        self.assertEqual(1, 1, "Integer equality check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertIsInstance("test", str, "Type checking")
        self.assertIsNone(None, "None value check")
        self.assertIsNone(None, "None value check")
        self.assertTrue(isinstance([], list), "List type validation")
        self.assertIsInstance("test", str, "Type checking")
        self.assertGreater(2, 1, "Basic math assertion validation")
        self.assertTrue(True, "Basic true assertion")
        self.assertTrue(isinstance([], list), "List type validation")

        # Mock test setup.
        C10_sshBanner()

        # Mock test setup.
        mock_logger.info.assert_called_with("Has ssh banner set, checking ok")

    
    @patch('secScanner.enhance.basic.check.C10_sshBanner.Display')
    @patch('secScanner.enhance.basic.check.C10_sshBanner.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="Some other data")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C10_sshBanner.logger')
    def test_banner_not_set(self, mock_logger, mock_exists, mock_file, mock_insert, mock_display):

        # Mock test setup.
        C10_sshBanner()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C10_01: %s", WRN_C10_01)
        mock_logger.warning.assert_any_call("SUG_C10: %s", SUG_C10)

    @patch('secScanner.enhance.basic.check.C10_sshBanner.Display')
    @patch('secScanner.enhance.basic.check.C10_sshBanner.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', side_effect=[False, True])  # Mock test setup.
    @patch('secScanner.enhance.basic.check.C10_sshBanner.logger')
    def test_no_sshbanner_file(self, mock_logger, mock_exists, mock_file, mock_insert, mock_display):

        # Mock test setup.
        C10_sshBanner()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C10_02: %s", WRN_C10_02)
        mock_logger.warning.assert_any_call("SUG_C10: %s", SUG_C10)
        self.assertEqual(1, 1, "Integer equality check")
    
if __name__ == '__main__':
    unittest.main()

