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
from secScanner.enhance.euler.check.C03508_icmpredirectfwd import C03508_icmpredirectfwd  # Mock test setup.

redirectParams = ["net.ipv4.conf.all.send_redirects",
                  "net.ipv4.conf.default.send_redirects"]


def _result(stdout):
    result = MagicMock()
    result.stdout = stdout
    return result


class TestC03508_icmpredirectfwd(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_not_set_to_0_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.side_effect = [_result(("%s = 1\n" % param).encode("utf-8")) for param in redirectParams]

        # Mock test setup.
        secScanner.enhance.euler.check.C03508_icmpredirectfwd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03508_icmpredirectfwd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not send ICMP redirect packets")
        warnMessage = [WRN_C03508_01, WRN_C03508_02]
        sugMessage = [SUG_C03508_01, SUG_C03508_02]
        self.assertEqual(mock_run.call_count, 2)
        for i in range(len(redirectParams)):
            param = redirectParams[i]
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
            mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
            mock_logger.warning.assert_any_call("WRN_C03508_0%d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C03508_0%d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- %s is not set to 0..." % param, "WARNING")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_file().write.assert_called_with("\nC03508\n")

    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_set_to_0_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.side_effect = [_result(("%s = 0\n" % param).encode("utf-8")) for param in redirectParams]

        # Mock test setup.
        secScanner.enhance.euler.check.C03508_icmpredirectfwd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03508_icmpredirectfwd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not send ICMP redirect packets")
        self.assertEqual(mock_run.call_count, 2)
        for param in redirectParams:
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
            mock_logger.info.assert_any_call("ICMP redirect send parameter (%s) is set to 0", param)
            mock_Display.assert_any_call("- Check whether %s is set to 0..." % param, "OK")
        mock_file.assert_not_called()
        mock_logger.warning.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.InsertSection')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.Display')
    @patch('secScanner.enhance.euler.check.C03508_icmpredirectfwd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_second_not_set_to_0_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：仅第二个参数非 0，只应写入一次结果并告警一次"""
        # Mock test setup.
        mock_run.side_effect = [
            _result(b"net.ipv4.conf.all.send_redirects = 0\n"),
            _result(b"net.ipv4.conf.default.send_redirects = 3\n"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03508_icmpredirectfwd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03508_icmpredirectfwd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the system does not send ICMP redirect packets")
        mock_file().write.assert_called_once_with("\nC03508\n")
        self.assertEqual(mock_logger.warning.call_count, 2)
        mock_logger.warning.assert_any_call("WRN_C03508_0%d: %s", 2, WRN_C03508_02)
        mock_logger.warning.assert_any_call("SUG_C03508_0%d: %s", 2, SUG_C03508_02)
        mock_Display.assert_any_call("- net.ipv4.conf.default.send_redirects is not set to 0...", "WARNING")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.all.send_redirects is set to 0...", "OK")

if __name__ == '__main__':
    unittest.main()
