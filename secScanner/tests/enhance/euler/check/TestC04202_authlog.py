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
from secScanner.enhance.euler.check.C04202_authlog import C04202_authlog  # Mock test setup.

CONFIG_FILE = "/etc/rsyslog.conf"
SECTION = "Check the auth events log config in /etc/rsyslog.conf"

class TestC04202_authlog(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.check.C04202_authlog.Display')
    @patch('secScanner.enhance.euler.check.C04202_authlog.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="*.info;mail.none           /var/log/messages\n")
    def test_auth_log_not_configured_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """不合规：rsyslog.conf 中无 auth 日志配置，应 WARNING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C04202_authlog.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04202_authlog()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call(CONFIG_FILE, 'r')
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04202\n")
        mock_logger.warning.assert_any_call("WRN_C04202: %s", WRN_C04202)
        mock_logger.warning.assert_any_call("SUG_C04202: %s", SUG_C04202)
        mock_Display.assert_called_once_with("- The auth events log is not recorded in /etc/rsyslog.conf...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.check.C04202_authlog.Display')
    @patch('secScanner.enhance.euler.check.C04202_authlog.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="*.info;mail.none           /var/log/messages\nauthpriv.*                     /var/log/secure\n")
    def test_auth_log_configured_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """合规：存在非注释 auth 配置，应 OK 且不写 RESULT_FILE"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C04202_authlog.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04202_authlog()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with(CONFIG_FILE, 'r')
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("The auth events log is recorded, checking OK")
        mock_Display.assert_called_once_with("- Check the auth events log config...", "OK")

    @patch('secScanner.enhance.euler.check.C04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.check.C04202_authlog.Display')
    @patch('secScanner.enhance.euler.check.C04202_authlog.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="#authpriv.*                     /var/log/secure\n\n*.info;mail.none           /var/log/messages\n")
    def test_auth_log_only_commented_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：auth 仅出现在注释行，非注释行不含 auth，应判为不合规"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C04202_authlog.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04202_authlog()

        # Mock test setup.
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04202\n")
        mock_logger.warning.assert_any_call("WRN_C04202: %s", WRN_C04202)
        mock_Display.assert_called_once_with("- The auth events log is not recorded in /etc/rsyslog.conf...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.check.C04202_authlog.Display')
    @patch('secScanner.enhance.euler.check.C04202_authlog.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C04202_authlog.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04202_authlog()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04202\n")
        mock_logger.warning.assert_any_call("WRN_C04202: %s %s", CONFIG_FILE, WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C04202: %s %s", CONFIG_FILE, SUG_no_file)
        mock_Display.assert_called_once_with(f"- {CONFIG_FILE} does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
