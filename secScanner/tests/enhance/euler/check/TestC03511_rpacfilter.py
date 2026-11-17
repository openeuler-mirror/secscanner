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
from secScanner.enhance.euler.check.C03511_rpacfilter import C03511_rpacfilter  # Mock test setup.


def _run_result(stdout=b"", returncode=0):
    result = Mock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestC03511_rpacfilter(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rp_filter_not_enabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 0\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 0\n"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03511_rpacfilter.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03511_rpacfilter()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the reverse path filtering is enabled")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['sysctl', "net.ipv4.conf.all.rp_filter"], capture_output=True)
        mock_run.assert_any_call(['sysctl', "net.ipv4.conf.default.rp_filter"], capture_output=True)
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_file().write.assert_any_call("\nC03511\n")
        warnMessage = [WRN_C03511_01, WRN_C03511_02]
        sugMessage = [SUG_C03511_01, SUG_C03511_02]
        for i in range(2):
            mock_logger.warning.assert_any_call("WRN_C03511_0%d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C03511_0%d: %s", (i + 1), sugMessage[i])
        rpParams = ["net.ipv4.conf.all.rp_filter", "net.ipv4.conf.default.rp_filter"]
        for param in rpParams:
            mock_Display.assert_any_call("- %s is not set to 1..." % param, "WARNING")

    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rp_filter_enabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 1\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 1\n"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03511_rpacfilter.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03511_rpacfilter()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the reverse path filtering is enabled")
        self.assertEqual(mock_logger.info.call_count, 2)
        rpParams = ["net.ipv4.conf.all.rp_filter", "net.ipv4.conf.default.rp_filter"]
        for param in rpParams:
            mock_logger.info.assert_any_call("Reverse path filtering parameter (%s) is set to 1", param)
            mock_Display.assert_any_call("- Check whether %s is set to 1..." % param, "OK")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.check.C03511_rpacfilter.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rp_filter_partial_compliant(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：all 不合规、default 合规，仅写入一次 RESULT_FILE"""
        # Mock test setup.
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 0\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 1\n"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03511_rpacfilter.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03511_rpacfilter()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03511\n")
        mock_Display.assert_any_call("- net.ipv4.conf.all.rp_filter is not set to 1...", "WARNING")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.default.rp_filter is set to 1...", "OK")


if __name__ == '__main__':
    unittest.main()
