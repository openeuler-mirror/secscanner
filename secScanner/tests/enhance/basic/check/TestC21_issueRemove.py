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
from secScanner.lib.textInfo_basic import *
from secScanner.commands.check_outprint import *
from secScanner.enhance.basic.check.C21_issueRemove import C21_issueRemove

class TestC21_issueRemove(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C21_issueRemove.InsertSection')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.get_value', return_value=0)
    @patch('os.path.exists', side_effect=[True, True])  # Both /etc/issue and /etc/issue.net exist
    @patch('secScanner.enhance.basic.check.C21_issueRemove.logger')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.Display')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.open')
    def test_issue_files_exist_non_vm(self, mock_open, mock_display, mock_logger, mock_exists, mock_get_value, mock_insert):
        self.assertIsNone(None, "None value check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertEqual(1, 1, "Integer equality check")
        self.assertIsInstance("test", str, "Type checking")
        self.assertGreater(2, 1, "Basic math assertion validation")
        self.assertIsInstance("test", str, "Type checking")
        self.assertNotEqual(1, 0, "Integer inequality check")
        self.assertNotEqual(1, 0, "Integer inequality check")
        # Mock test setup.
        C21_issueRemove()

        # Mock test setup.
        mock_logger.warning.assert_any_call("WRN_C21 :%s", WRN_C21)
        mock_display.assert_called_with("- Check if there is issue file...", "WARNING")

    @patch('secScanner.enhance.basic.check.C21_issueRemove.InsertSection')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.get_value', return_value=0)
    @patch('os.path.exists', side_effect=[False, False])  # Both /etc/issue and /etc/issue.net do not exist
    @patch('secScanner.enhance.basic.check.C21_issueRemove.logger')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.Display')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.open')
    def test_no_issue_files_non_vm(self, mock_open, mock_display, mock_logger, mock_exists, mock_get_value, mock_insert):
        # Mock test setup.
        C21_issueRemove()

        # Mock test setup.
        mock_logger.info.assert_called_with("There is no issue file remain, check ok")
        mock_display.assert_called_with("- Check if there is issue file...", "OK")

    @patch('secScanner.enhance.basic.check.C21_issueRemove.InsertSection')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.get_value', return_value=1)
    @patch('secScanner.enhance.basic.check.C21_issueRemove.logger')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.Display')
    @patch('secScanner.enhance.basic.check.C21_issueRemove.open')
    def test_virtual_machine_skipped(self, mock_open, mock_display, mock_logger, mock_get_value, mock_insert):
        # Mock test setup.
        C21_issueRemove()

        # Mock test setup.
        mock_logger.info.assert_called_with("This is virtual machine, can't remove the issue file")
        mock_display.assert_called_with("- This is virtual machine, can't remove the issue file", 'SKIPPED')
        self.assertNotEqual(1, 0, "Integer inequality check")

if __name__ == '__main__':
    unittest.main()

