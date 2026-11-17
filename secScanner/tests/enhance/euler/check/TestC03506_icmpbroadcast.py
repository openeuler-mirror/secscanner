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
from secScanner.enhance.euler.check.C03506_icmpbroadcast import C03506_icmpbroadcast  # Mock test setup.


class TestC03506_icmpbroadcast(unittest.TestCase):

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.InsertSection')
    def test_icmpbroadcast_disabled_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_run, mock_file):
        """不合规：net.ipv4.icmp_echo_ignore_broadcasts 为 0，应 WARNING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_run.return_value.stdout = b"net.ipv4.icmp_echo_ignore_broadcasts = 0\n"
        result_handle = mock_open().return_value
        mock_file.return_value = result_handle
        secScanner.enhance.euler.check.C03506_icmpbroadcast.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not respond ICMP broadcast packets")
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.icmp_echo_ignore_broadcasts'], capture_output=True)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        result_handle.write.assert_called_once_with("\nC03506\n")
        mock_logger.warning.assert_any_call("WRN_C03506: %s", WRN_C03506)
        mock_logger.warning.assert_any_call("SUG_C03506: %s", SUG_C03506)
        mock_Display.assert_called_once_with("- The system responds to ICMP broadcast packets...", "WARNING")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.InsertSection')
    def test_icmpbroadcast_already_ignored_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_run, mock_file):
        """合规：net.ipv4.icmp_echo_ignore_broadcasts 为 1，应 OK 且不写 RESULT_FILE"""
        # Mock test setup.
        mock_run.return_value.stdout = b"net.ipv4.icmp_echo_ignore_broadcasts = 1\n"
        result_handle = mock_open().return_value
        mock_file.return_value = result_handle
        secScanner.enhance.euler.check.C03506_icmpbroadcast.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not respond ICMP broadcast packets")
        result_handle.write.assert_not_called()
        mock_logger.info.assert_called_once_with("The system does not respond to ICMP broadcast packets")
        mock_Display.assert_called_once_with("- Check whether the system does not respond ICMP broadcast packets...", "OK")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.InsertSection')
    def test_icmpbroadcast_crlf_output_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_run, mock_file):
        """边界：输出以 CRLF 结尾时经 strip 处理后仍判定为合规"""
        # Mock test setup.
        mock_run.return_value.stdout = b"net.ipv4.icmp_echo_ignore_broadcasts = 1\r\n"
        result_handle = mock_open().return_value
        mock_file.return_value = result_handle
        secScanner.enhance.euler.check.C03506_icmpbroadcast.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not respond ICMP broadcast packets")
        result_handle.write.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the system does not respond ICMP broadcast packets...", "OK")

    @patch('builtins.open')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.check.C03506_icmpbroadcast.InsertSection')
    def test_icmpbroadcast_multidigit_value_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_run, mock_file):
        """边界：取值非个位数时仅以末位判断，10 应视为不合规"""
        # Mock test setup.
        mock_run.return_value.stdout = b"net.ipv4.icmp_echo_ignore_broadcasts = 10\n"
        result_handle = mock_open().return_value
        mock_file.return_value = result_handle
        secScanner.enhance.euler.check.C03506_icmpbroadcast.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not respond ICMP broadcast packets")
        result_handle.write.assert_called_once_with("\nC03506\n")
        mock_Display.assert_called_once_with("- The system responds to ICMP broadcast packets...", "WARNING")

if __name__ == '__main__':
    unittest.main()
