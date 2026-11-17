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
from secScanner.enhance.euler.check.C04111_logsizelimit import C04111_logsizelimit  # Mock test setup.

CONFIG_FILE = "/etc/audit/auditd.conf"
SECTION = "Check the audit log size limit config in /etc/audit/auditd.conf"

class TestC04111_logsizelimit(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="max_log_file = abc\n")
    def test_invalid_max_log_file_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """不合规：max_log_file 非数字，应 WARNING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C04111_logsizelimit.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04111\n")
        mock_logger.warning.assert_any_call("WRN_C04111: %s", WRN_C04111)
        mock_logger.warning.assert_any_call("SUG_C04111: %s", SUG_C04111)
        mock_Display.assert_called_once_with("- The max_log_file of audit log size limit is not safe...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="# auditd.conf\nmax_log_file = 8\n")
    def test_valid_max_log_file_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """合规：max_log_file 为正整数，注释行被忽略，应 OK 且不写 RESULT_FILE"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("The max_log_file of audit log size limit is safe, checking OK")
        mock_Display.assert_called_once_with("- Check the max_log_file of audit log size limit...", "OK")

    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="max_log_file = 0\n")
    def test_max_log_file_zero_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：max_log_file 为 0（是数字但不大于 0），应判为不合规"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C04111_logsizelimit.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04111\n")
        mock_Display.assert_called_once_with("- The max_log_file of audit log size limit is not safe...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.check.C04111_logsizelimit.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C04111_logsizelimit.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04111\n")
        mock_logger.warning.assert_any_call("WRN_C04111: %s %s", CONFIG_FILE, WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C04111: %s %s", CONFIG_FILE, SUG_no_file)
        mock_Display.assert_called_once_with(f"- {CONFIG_FILE} does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
