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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03520_coredump import C03520_coredump  # Mock test setup.

class TestC03520_coredump(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.stat')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.check.C03520_coredump.Display')
    @patch('secScanner.enhance.euler.check.C03520_coredump.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_core_dump_not_safe(self, mock_file, mock_logger, mock_Display,
                                mock_InsertSection, mock_exists, mock_isdir,
                                mock_stat, mock_run):
        # Mock test setup.
        mock_run.side_effect = [
            MagicMock(stdout=b'1024\n'),
            MagicMock(stdout=b'kernel.core_pattern = /var/crash/core\n'),
        ]
        mock_exists.side_effect = lambda path: path == "/etc/security/limits.conf"
        mock_isdir.return_value = True
        mock_stat.return_value.st_mode = 0o40755

        # Mock test setup.
        secScanner.enhance.euler.check.C03520_coredump.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the core dump config is right")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03520\n")
        mock_logger.warning.assert_any_call("WRN_C03520: %s", WRN_C03520)
        mock_logger.warning.assert_any_call("SUG_C03520: %s", SUG_C03520)
        mock_Display.assert_called_once_with("- The core dump config is not safe...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.check.C03520_coredump.Display')
    @patch('secScanner.enhance.euler.check.C03520_coredump.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_ulimit_zero_disabled(self, mock_file, mock_logger, mock_Display,
                                  mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = MagicMock(stdout=b'0\n')

        # Mock test setup.
        C03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the core dump config is right")
        mock_run.assert_called_once_with("ulimit -c", shell=True, capture_output=True)
        mock_logger.info.assert_called_once_with("Core dump is disabled")
        mock_Display.assert_called_once_with("- Check whether the core dump config is right...", "OK")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.check.C03520_coredump.Display')
    @patch('secScanner.enhance.euler.check.C03520_coredump.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="*   hard   core   0\n")
    def test_limits_conf_disabled(self, mock_file, mock_logger, mock_Display,
                                  mock_InsertSection, mock_exists, mock_run):
        """边界：ulimit 非 0，但 limits.conf 已配置 hard core 0，应视为已禁用"""
        # Mock test setup.
        mock_run.return_value = MagicMock(stdout=b'unlimited\n')
        mock_exists.return_value = True

        # Mock test setup.
        C03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the core dump config is right")
        mock_run.assert_called_once_with("ulimit -c", shell=True, capture_output=True)
        mock_logger.info.assert_called_once_with("Core dump is disabled")
        mock_Display.assert_called_once_with("- Check whether the core dump config is right...", "OK")
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03520_coredump.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.stat')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C03520_coredump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03520_coredump.InsertSection')
    @patch('secScanner.enhance.euler.check.C03520_coredump.Display')
    @patch('secScanner.enhance.euler.check.C03520_coredump.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_core_dump_dir_mode_700(self, mock_file, mock_logger, mock_Display,
                                    mock_InsertSection, mock_exists, mock_isdir,
                                    mock_stat, mock_run):
        """边界：core 目录权限为 700，应判定为安全"""
        # Mock test setup.
        mock_run.side_effect = [
            MagicMock(stdout=b'1024\n'),
            MagicMock(stdout=b'kernel.core_pattern = /var/crash/core\n'),
        ]
        mock_exists.return_value = False
        mock_isdir.return_value = True
        mock_stat.return_value.st_mode = 0o40700

        # Mock test setup.
        C03520_coredump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the core dump config is right")
        mock_logger.info.assert_called_once_with("Core dump path is limited safely")
        mock_Display.assert_called_once_with("- Check whether the core dump config is right...", "OK")
        mock_file().write.assert_not_called()

if __name__ == '__main__':
    unittest.main()
