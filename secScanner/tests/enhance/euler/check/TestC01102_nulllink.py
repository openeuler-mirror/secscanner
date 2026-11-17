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
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01102_nulllink import C01102_nulllink  # Mock test setup.

class TestC01102_nulllink(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.Display')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_nulllink_found(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '/tmp/broken_link')

        # Mock test setup.
        secScanner.enhance.euler.check.C01102_nulllink.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are null link files")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01102\n")
        mock_logger.warning.assert_any_call("WRN_C01102: %s", WRN_C01102)
        mock_logger.warning.assert_any_call("SUG_C01102: %s", SUG_C01102)
        mock_Display.assert_called_once_with("- Found null link files in your Linux System...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.Display')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.logger')
    def test_no_nulllink_found(self, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        C01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are null link files")
        mock_logger.info.assert_called_once_with("No null link file found, checking ok")
        mock_Display.assert_called_once_with("- Check whether null link files exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.Display')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.logger')
    def test_find_command_failed(self, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, '')

        # Mock test setup.
        C01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are null link files")
        mock_Display.assert_called_once_with("- Check whether null link files exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.Display')
    @patch('secScanner.enhance.euler.check.C01102_nulllink.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_nulllink_found_whitespace_only(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：find 输出仅空白字符应视为无空链文件"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, ' \n\t')

        # Mock test setup.
        C01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are null link files")
        mock_Display.assert_called_once_with("- Check whether null link files exist...", "OK")

if __name__ == '__main__':
    unittest.main()
