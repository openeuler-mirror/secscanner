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
from unittest.mock import patch, MagicMock
import logging
from secScanner.enhance.euler.set.S03512_ipforward import S03512_ipforward  # Mock test setup.


def _run_result(output, returncode=0):
    mock_result = MagicMock()
    mock_result.stdout.strip.return_value.decode.return_value = output
    mock_result.returncode = returncode
    return mock_result


class TestS03512_ipforward(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03512_ipforward._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.Display')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.logger')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03512_ipforward()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_ipforward')
        mock_InsertSection.assert_called_once_with("Set the IP forwarding disabled...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set IP forwarding parameters due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03512_ipforward._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.Display')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.logger')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result("net.ipv4.ip_forward = 1"),
            _run_result("net.ipv6.conf.all.forwarding = 1"),
            _run_result("net.ipv4.ip_forward = 0", 0),
            _run_result("net.ipv6.conf.all.forwarding = 0", 0),
            _run_result("net.ipv4.route.flush = 1", 0),
            _run_result("net.ipv6.route.flush = 1", 0),
        ]

        # Mock test setup.
        S03512_ipforward()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_ipforward')
        mock_InsertSection.assert_called_once_with("Set the IP forwarding disabled...")
        mock_run.assert_any_call(['sysctl', 'net.ipv4.ip_forward'], capture_output=True)
        mock_run.assert_any_call(['sysctl', 'net.ipv6.conf.all.forwarding'], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.ip_forward=0"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv6.conf.all.forwarding=0"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.route.flush=1"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv6.route.flush=1"], capture_output=True)
        self.assertEqual(mock_run.call_count, 6)
        mock_persist.assert_called_once_with([('net.ipv4.ip_forward', 'net.ipv4.ip_forward=0'),
                                             ('net.ipv6.conf.all.forwarding', 'net.ipv6.conf.all.forwarding=0')])
        mock_logger.info.assert_any_call("Set IP forwarding parameters finish")
        mock_Display.assert_called_once_with("- Set IP forwarding parameters to 0...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03512_ipforward._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.Display')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.logger')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result("net.ipv4.ip_forward = 1"),
            _run_result("net.ipv6.conf.all.forwarding = 1"),
            _run_result("", 1),
            _run_result("", 1),
            _run_result("", 0),
            _run_result("", 0),
        ]

        # Mock test setup.
        S03512_ipforward()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_ipforward')
        mock_InsertSection.assert_called_once_with("Set the IP forwarding disabled...")
        mock_logger.warning.assert_called_once_with("Set IP forwarding parameters failed")
        mock_Display.assert_called_once_with("- Set IP forwarding parameters to 0...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03512_ipforward._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.InsertSection')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.Display')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.logger')
    @patch('secScanner.enhance.euler.set.S03512_ipforward.seconf.get')
    def test_already_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """边界：参数已全部为 0，无需设置，应跳过且不写入持久化配置"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result("net.ipv4.ip_forward = 0"),
            _run_result("net.ipv6.conf.all.forwarding = 0"),
        ]

        # Mock test setup.
        S03512_ipforward()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_ipforward')
        mock_InsertSection.assert_called_once_with("Set the IP forwarding disabled...")
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.info.assert_any_call("IP forwarding parameters already set to 0")
        mock_Display.assert_called_once_with("- IP forwarding parameters have already been set to 0...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
