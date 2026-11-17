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
from secScanner.enhance.euler.check.C03510_bogusicmp import C03510_bogusicmp  # Mock test setup.


def _run_result(stdout=b"", returncode=0):
    result = Mock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestC03510_bogusicmp(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_bogus_icmp_not_ignored(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 0\n")

        # Mock test setup.
        secScanner.enhance.euler.check.C03510_bogusicmp.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03510_bogusicmp()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the bogus ICMP responses are ignored")
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.icmp_ignore_bogus_error_responses'], capture_output=True)
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03510\n")
        mock_logger.warning.assert_any_call("WRN_C03510: %s", WRN_C03510)
        mock_logger.warning.assert_any_call("SUG_C03510: %s", SUG_C03510)
        mock_Display.assert_called_once_with("- The system does not ignore bogus ICMP responses...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_bogus_icmp_ignored(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 1\n")

        # Mock test setup.
        secScanner.enhance.euler.check.C03510_bogusicmp.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03510_bogusicmp()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the bogus ICMP responses are ignored")
        mock_logger.info.assert_called_once_with("The system ignores bogus ICMP responses")
        mock_Display.assert_called_once_with("- Check whether the bogus ICMP responses are ignored...", "OK")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_bogus_icmp_ignored_with_trailing_blank(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：sysctl 输出带尾随空行，strip 后末位仍为 1，应判定为 OK"""
        # Mock test setup.
        mock_run.return_value = _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 1\n\n")

        # Mock test setup.
        secScanner.enhance.euler.check.C03510_bogusicmp.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03510_bogusicmp()

        # Mock test setup.
        mock_Display.assert_called_once_with("- Check whether the bogus ICMP responses are ignored...", "OK")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.check.C03510_bogusicmp.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_bogus_icmp_unknown_value_not_ignored(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：末位为其他字符（非 1）时按不合规处理并写入 RESULT_FILE"""
        # Mock test setup.
        mock_run.return_value = _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 2\n")

        # Mock test setup.
        secScanner.enhance.euler.check.C03510_bogusicmp.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03510_bogusicmp()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03510\n")
        mock_Display.assert_called_once_with("- The system does not ignore bogus ICMP responses...", "WARNING")


if __name__ == '__main__':
    unittest.main()
