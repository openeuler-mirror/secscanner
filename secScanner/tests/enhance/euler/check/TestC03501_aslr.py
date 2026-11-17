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
import logging
import secScanner
import secScanner.enhance.euler.check.C03501_aslr as C03501_module
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03501_aslr import C03501_aslr

RESULT = "check_result.relt"


def _make_run(stdout):
    result = MagicMock()
    result.stdout = stdout
    result.returncode = 0
    return result


class TestC03501_aslr(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.check.C03501_aslr.Display')
    @patch('secScanner.enhance.euler.check.C03501_aslr.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_aslr_not_fully_enabled_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = _make_run(b"kernel.randomize_va_space = 0\n")

        # Mock test setup.
        C03501_module.RESULT_FILE = RESULT

        # Mock test setup.
        C03501_aslr()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel ASLR is enabled")
        mock_run.assert_called_once_with(['sysctl', 'kernel.randomize_va_space'], capture_output=True)
        mock_file.assert_called_with(RESULT, "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03501\n")
        mock_logger.warning.assert_any_call("WRN_C03501: %s", WRN_C03501)
        mock_logger.warning.assert_any_call("SUG_C03501: %s", SUG_C03501)
        mock_Display.assert_called_once_with("- The kernel ASLR is not fully enabled...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.check.C03501_aslr.Display')
    @patch('secScanner.enhance.euler.check.C03501_aslr.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_aslr_enabled_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = _make_run(b"kernel.randomize_va_space = 2\n")

        # Mock test setup.
        C03501_module.RESULT_FILE = RESULT

        # Mock test setup.
        C03501_aslr()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel ASLR is enabled")
        mock_run.assert_called_once_with(['sysctl', 'kernel.randomize_va_space'], capture_output=True)
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The kernel ASLR is enabled")
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the kernel ASLR is enabled...", "OK")

    @patch('secScanner.enhance.euler.check.C03501_aslr.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03501_aslr.InsertSection')
    @patch('secScanner.enhance.euler.check.C03501_aslr.Display')
    @patch('secScanner.enhance.euler.check.C03501_aslr.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_aslr_value_without_key_name_boundary(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：sysctl 输出仅含单个字符 2（无键名、无换行），应判定为已启用"""
        # Mock test setup.
        mock_run.return_value = _make_run(b"2")

        # Mock test setup.
        C03501_module.RESULT_FILE = RESULT

        # Mock test setup.
        C03501_aslr()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the kernel ASLR is enabled")
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the kernel ASLR is enabled...", "OK")

if __name__ == '__main__':
    unittest.main()
