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
from secScanner.enhance.euler.check.C04201_rsyslogd import C04201_rsyslogd  # Mock test setup.

SECTION = "Check the rsyslog service status in your Linux System"

class TestC04201_rsyslogd(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rsyslog_not_installed_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """不合规：rsyslog 未安装，应 WARNING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, 'package rsyslog is not installed')

        # Mock test setup.
        secScanner.enhance.euler.check.C04201_rsyslogd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04201_rsyslogd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_getstatusoutput.assert_called_once_with('rpm -q rsyslog')
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04201\n")
        mock_logger.warning.assert_any_call("WRN_C04201_01: %s", WRN_C04201_01)
        mock_logger.warning.assert_any_call("SUG_C04201_01: %s", SUG_C04201_01)
        mock_Display.assert_called_once_with("- The status of rsyslog is :package rsyslog is not installed not installed...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rsyslog_installed_enabled_active_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """合规：已安装、已 enable、已 active，应三次 OK 且不写 RESULT_FILE"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (0, 'enabled'),
                                           (0, 'active')]

        # Mock test setup.
        C04201_rsyslogd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        self.assertEqual(mock_getstatusoutput.call_count, 3)
        mock_getstatusoutput.assert_any_call('rpm -q rsyslog')
        mock_getstatusoutput.assert_any_call('systemctl is-enabled rsyslog.service')
        mock_getstatusoutput.assert_any_call('systemctl is-active rsyslog.service')
        mock_file().write.assert_not_called()
        mock_Display.assert_any_call("- Check the rsyslog software is installed...", "OK")
        mock_Display.assert_any_call("- Check the rsyslog service is enabled...", "OK")
        mock_Display.assert_any_call("- Check the rsyslog service is active...", "OK")

    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rsyslog_disabled_but_active_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """不合规：服务未 enabled 但已 active，应只记录 C04201_02 并写一次 RESULT_FILE"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'disabled'),
                                           (0, 'active')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04201_rsyslogd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04201_rsyslogd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04201\n")
        mock_logger.warning.assert_any_call("WRN_C04201_02: %s", WRN_C04201_02)
        mock_logger.warning.assert_any_call("SUG_C04201_02: %s", SUG_C04201_02)
        mock_Display.assert_any_call("- Check the rsyslog software is installed...", "OK")
        mock_Display.assert_any_call("- Check the status of rsyslog is disabled...", "WARNING")
        mock_Display.assert_any_call("- Check the rsyslog service is active...", "OK")

    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rsyslog_enabled_bit_set_but_return_code_failed(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：is-enabled 输出为 enabled 但返回码非 0，应仍判为不合规"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'enabled'),
                                           (0, 'active')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04201_rsyslogd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04201_rsyslogd()

        # Mock test setup.
        mock_file().write.assert_called_once_with("\nC04201\n")
        mock_logger.warning.assert_any_call("WRN_C04201_02: %s", WRN_C04201_02)
        mock_Display.assert_any_call("- Check the status of rsyslog is enabled...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.check.C04201_rsyslogd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rsyslog_disabled_and_inactive_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """不合规：服务既未 enabled 也未 active，应写两次 RESULT_FILE 记录两条告警"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'disabled'),
                                           (3, 'inactive')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04201_rsyslogd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04201_rsyslogd()

        # Mock test setup.
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_logger.warning.assert_any_call("WRN_C04201_02: %s", WRN_C04201_02)
        mock_logger.warning.assert_any_call("WRN_C04201_03: %s", WRN_C04201_03)
        mock_Display.assert_any_call("- Check the status of rsyslog is inactive...", "WARNING")

if __name__ == '__main__':
    unittest.main()
