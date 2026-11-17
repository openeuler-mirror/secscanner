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
from secScanner.enhance.euler.check.C03512_ipforward import C03512_ipforward  # Mock test setup.


def _sysctl_result(output):
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value.decode.return_value = output
    return mock_result


class TestC03512_ipforward(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.Display')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_ipforward_not_set_to_zero_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """不符合：两个转发参数均不为 0，应告警并写入 RESULT_FILE"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.ip_forward = 1"),
            _sysctl_result("net.ipv6.conf.all.forwarding = 2"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03512_ipforward.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03512_ipforward()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP forwarding is disabled")
        forwardParams = ["net.ipv4.ip_forward", "net.ipv6.conf.all.forwarding"]
        warnMessage = [WRN_C03512_01, WRN_C03512_02]
        sugMessage = [SUG_C03512_01, SUG_C03512_02]
        for i in range(len(forwardParams)):
            param = forwardParams[i]
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
            mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
            mock_logger.warning.assert_any_call("WRN_C03512_0%d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C03512_0%d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- %s is not set to 0..." % param, "WARNING")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_file().write.assert_any_call("\nC03512\n")

    @patch('secScanner.enhance.euler.check.C03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.Display')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_ipforward_set_to_zero_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """符合：两个转发参数均为 0，不应告警"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.ip_forward = 0"),
            _sysctl_result("net.ipv6.conf.all.forwarding = 0"),
        ]

        # Mock test setup.
        C03512_ipforward()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP forwarding is disabled")
        forwardParams = ["net.ipv4.ip_forward", "net.ipv6.conf.all.forwarding"]
        for param in forwardParams:
            mock_logger.info.assert_any_call("IP forwarding parameter (%s) is set to 0", param)
            mock_Display.assert_any_call("- Check whether %s is set to 0..." % param, "OK")
        mock_logger.warning.assert_not_called()
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.Display')
    @patch('secScanner.enhance.euler.check.C03512_ipforward.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_ipforward_value_ending_with_zero_boundary(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：取输出末位字符判断，末位为 0 的非 0 值(如 10)会被判为合规"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.ip_forward = 10"),
            _sysctl_result("net.ipv6.conf.all.forwarding = 0"),
        ]

        # Mock test setup.
        C03512_ipforward()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP forwarding is disabled")
        mock_Display.assert_any_call("- Check whether net.ipv4.ip_forward is set to 0...", "OK")
        mock_Display.assert_any_call("- Check whether net.ipv6.conf.all.forwarding is set to 0...", "OK")
        mock_logger.warning.assert_not_called()
        mock_file().write.assert_not_called()


if __name__ == '__main__':
    unittest.main()
