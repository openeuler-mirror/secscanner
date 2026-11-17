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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01113_suidsgid import C01113_suidsgid  # Mock test setup.

class TestC01113_suidsgid(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_suid_sgid_files_found(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '/usr/bin/su\n/usr/bin/foobar')

        # Mock test setup.
        secScanner.enhance.euler.check.C01113_suidsgid.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01113_suidsgid()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files with SUID and SGID bits set")
        mock_getstatusoutput.assert_called_once_with(
            "find / -type f \\( -perm -4000 -o -perm -2000 \\) 2>/dev/null")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01113\n")
        mock_logger.warning.assert_any_call("WRN_C01113: %s", WRN_C01113)
        mock_logger.warning.assert_any_call("SUG_C01113: %s", SUG_C01113)
        mock_Display.assert_any_call("- Found files with SUID or SGID bits set in your Linux System...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_suid_sgid_files(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        C01113_suidsgid()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files with SUID and SGID bits set")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("No file with SUID or SGID bits found, checking ok")
        mock_Display.assert_called_once_with("- Check whether files with SUID and SGID bits exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.check.C01113_suidsgid.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_find_command_failed_with_whitespace_output(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：find 返回非 0 且输出仅空白字符，应视为未发现并判定 OK"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, ' \n\t')

        # Mock test setup.
        C01113_suidsgid()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are files with SUID and SGID bits set")
        mock_file().write.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether files with SUID and SGID bits exist...", "OK")

if __name__ == '__main__':
    unittest.main()
