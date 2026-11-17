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
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01103_hiddenexec import C01103_hiddenexec  # Mock test setup.

class TestC01103_hiddenexec(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_hidden_exec_disabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '.bashrc\n.bash_profile\n.bash_logout')

        # Mock test setup.
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"  # Mock test setup.

        # Mock test setup.
        C01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_getstatusoutput.assert_called_once_with("find / -type f -name '\\.*' -perm /+x 2>/dev/null")
        mock_file.assert_not_called()
        mock_Display.assert_any_call("- Check whether hidden executable files exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_hidden_exec_enabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, '/home/user/.hidden_app')

        # Mock test setup.
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"  # Mock test setup.

        # Mock test setup.
        C01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_logger.warning.assert_any_call("WRN_C01103: %s", WRN_C01103)
        mock_logger.warning.assert_any_call("SUG_C01103: %s", SUG_C01103)
        mock_Display.assert_any_call("- Found hidden executable files in your Linux System...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_003_hiddenexec_subprocess_error(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """subprocess 返回非零退出码，视为检查通过"""
        mock_getstatusoutput.return_value = (1, '')
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"
        C01103_hiddenexec()
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_file.assert_not_called()
        mock_Display.assert_any_call("- Check whether hidden executable files exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_004_hiddenexec_empty_output(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """find 输出为空，视为检查通过"""
        mock_getstatusoutput.return_value = (0, '')
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"
        C01103_hiddenexec()
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_file.assert_not_called()
        mock_Display.assert_any_call("- Check whether hidden executable files exist...", "OK")

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_005_hiddenexec_multiple_entries(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """多个隐藏可执行文件（含 except_files 之外的），应触发 WARNING"""
        mock_getstatusoutput.return_value = (0, '/home/user/.bashrc\n/home/user/.hidden_app\n/etc/profile.d/.run_once')
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"
        C01103_hiddenexec()
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_Display.assert_any_call("- Found hidden executable files in your Linux System...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.check.C01103_hiddenexec.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_006_hiddenexec_trailing_spaces(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """输出末尾有多余空格，仍应触发 WARNING"""
        mock_getstatusoutput.return_value = (0, '/home/user/.hidden_file   ')
        secScanner.enhance.euler.check.C01103_hiddenexec.RESULT_FILE = "check_result.relt"
        C01103_hiddenexec()
        mock_InsertSection.assert_called_once_with("Check whether there are hidden executable files")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_Display.assert_any_call("- Found hidden executable files in your Linux System...", "WARNING")

if __name__ == '__main__':
    unittest.main()
