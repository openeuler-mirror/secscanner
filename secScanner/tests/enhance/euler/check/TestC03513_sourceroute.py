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
from secScanner.enhance.euler.check.C03513_sourceroute import C03513_sourceroute  # Mock test setup.


def _sysctl_result(output):
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value.decode.return_value = output
    return mock_result


class TestC03513_sourceroute(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03513_sourceroute.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.InsertSection')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.Display')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_sourceroute_not_set_to_zero_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """不符合：四个源路由参数均不为 0，应告警并写入 RESULT_FILE"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.conf.all.accept_source_route = 1"),
            _sysctl_result("net.ipv4.conf.default.accept_source_route = 1"),
            _sysctl_result("net.ipv6.conf.all.accept_source_route = 1"),
            _sysctl_result("net.ipv6.conf.default.accept_source_route = 1"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03513_sourceroute.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03513_sourceroute()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP source routing is disabled")
        routeParams = ["net.ipv4.conf.all.accept_source_route",
                       "net.ipv4.conf.default.accept_source_route",
                       "net.ipv6.conf.all.accept_source_route",
                       "net.ipv6.conf.default.accept_source_route"]
        warnMessage = [WRN_C03513_01, WRN_C03513_02, WRN_C03513_03, WRN_C03513_04]
        sugMessage = [SUG_C03513_01, SUG_C03513_02, SUG_C03513_03, SUG_C03513_04]
        for i in range(len(routeParams)):
            param = routeParams[i]
            mock_run.assert_any_call(['sysctl', param], capture_output=True)
            mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
            mock_logger.warning.assert_any_call("WRN_C03513_0%d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C03513_0%d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- %s is not set to 0..." % param, "WARNING")
        self.assertEqual(mock_file().write.call_count, 4)
        mock_file().write.assert_any_call("\nC03513\n")

    @patch('secScanner.enhance.euler.check.C03513_sourceroute.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.InsertSection')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.Display')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_sourceroute_set_to_zero_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """符合：四个源路由参数均为 0，不应告警"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.conf.all.accept_source_route = 0"),
            _sysctl_result("net.ipv4.conf.default.accept_source_route = 0"),
            _sysctl_result("net.ipv6.conf.all.accept_source_route = 0"),
            _sysctl_result("net.ipv6.conf.default.accept_source_route = 0"),
        ]

        # Mock test setup.
        C03513_sourceroute()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP source routing is disabled")
        routeParams = ["net.ipv4.conf.all.accept_source_route",
                       "net.ipv4.conf.default.accept_source_route",
                       "net.ipv6.conf.all.accept_source_route",
                       "net.ipv6.conf.default.accept_source_route"]
        for param in routeParams:
            mock_logger.info.assert_any_call("IP source route parameter (%s) is set to 0", param)
            mock_Display.assert_any_call("- Check whether %s is set to 0..." % param, "OK")
        mock_logger.warning.assert_not_called()
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C03513_sourceroute.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.InsertSection')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.Display')
    @patch('secScanner.enhance.euler.check.C03513_sourceroute.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_sourceroute_partial_zero_boundary(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：前三个参数为 0，仅最后一个不为 0，只应告警一次"""
        # Mock test setup.
        mock_run.side_effect = [
            _sysctl_result("net.ipv4.conf.all.accept_source_route = 0"),
            _sysctl_result("net.ipv4.conf.default.accept_source_route = 0"),
            _sysctl_result("net.ipv6.conf.all.accept_source_route = 0"),
            _sysctl_result("net.ipv6.conf.default.accept_source_route = 1"),
        ]

        # Mock test setup.
        secScanner.enhance.euler.check.C03513_sourceroute.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03513_sourceroute()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the IP source routing is disabled")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.all.accept_source_route is set to 0...", "OK")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.default.accept_source_route is set to 0...", "OK")
        mock_Display.assert_any_call("- Check whether net.ipv6.conf.all.accept_source_route is set to 0...", "OK")
        mock_Display.assert_any_call("- net.ipv6.conf.default.accept_source_route is not set to 0...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C03513_0%d: %s", 4, WRN_C03513_04)
        self.assertEqual(mock_file().write.call_count, 1)
        mock_file().write.assert_called_once_with("\nC03513\n")


if __name__ == '__main__':
    unittest.main()
