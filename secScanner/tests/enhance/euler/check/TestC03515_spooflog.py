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
from unittest.mock import patch, mock_open, Mock
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03515_spooflog import C03515_spooflog

class TestC03515_spooflog(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.Display')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_both_params_disabled_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """不合规：两个 log_martians 参数均为 0，应两次告警并写入 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 0")]

        secScanner.enhance.euler.check.C03515_spooflog.RESULT_FILE = "check_result.relt"

        C03515_spooflog()

        mock_InsertSection.assert_called_once_with("Check whether the spoofing, source-routed and redirect packets are logged")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['sysctl', 'net.ipv4.conf.all.log_martians'], capture_output=True)
        mock_run.assert_any_call(['sysctl', 'net.ipv4.conf.default.log_martians'], capture_output=True)
        self.assertEqual(mock_file().write.call_count, 2)
        mock_file().write.assert_any_call("\nC03515\n")
        mock_logger.warning.assert_any_call("WRN_C03515_0%d: %s", 1, WRN_C03515_01)
        mock_logger.warning.assert_any_call("SUG_C03515_0%d: %s", 1, SUG_C03515_01)
        mock_logger.warning.assert_any_call("WRN_C03515_0%d: %s", 2, WRN_C03515_02)
        mock_logger.warning.assert_any_call("SUG_C03515_0%d: %s", 2, SUG_C03515_02)
        mock_Display.assert_any_call("- net.ipv4.conf.all.log_martians is not set to 1...", "WARNING")
        mock_Display.assert_any_call("- net.ipv4.conf.default.log_martians is not set to 1...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.Display')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_both_params_enabled_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """合规：两个 log_martians 参数均为 1，不写 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 1"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 1")]

        C03515_spooflog()

        mock_InsertSection.assert_called_once_with("Check whether the spoofing, source-routed and redirect packets are logged")
        mock_file.assert_not_called()
        mock_logger.info.assert_any_call("Log martians parameter (%s) is set to 1", "net.ipv4.conf.all.log_martians")
        mock_logger.info.assert_any_call("Log martians parameter (%s) is set to 1", "net.ipv4.conf.default.log_martians")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.all.log_martians is set to 1...", "OK")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.default.log_martians is set to 1...", "OK")

    @patch('secScanner.enhance.euler.check.C03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.Display')
    @patch('secScanner.enhance.euler.check.C03515_spooflog.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_one_param_disabled_one_enabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：仅 all 参数不合规且输出带尾随空白，应只告警一次并写一次 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 0\n"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 1")]

        secScanner.enhance.euler.check.C03515_spooflog.RESULT_FILE = "check_result.relt"

        C03515_spooflog()

        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03515\n")
        mock_Display.assert_any_call("- net.ipv4.conf.all.log_martians is not set to 1...", "WARNING")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.default.log_martians is set to 1...", "OK")

if __name__ == '__main__':
    unittest.main()
