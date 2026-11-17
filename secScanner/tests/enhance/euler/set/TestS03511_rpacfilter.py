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
from unittest.mock import patch, Mock
import logging
from secScanner.enhance.euler.set.S03511_rpacfilter import S03511_rpacfilter  # Mock test setup.


def _run_result(stdout=b"", returncode=0):
    result = Mock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestS03511_rpacfilter(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03511_rpacfilter._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.logger')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03511_rpacfilter()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_rpacfilter')
        mock_InsertSection.assert_called_once_with("Set the reverse path filtering enabled...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with(
            "- Skip set reverse path filtering parameters due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03511_rpacfilter._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.logger')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.seconf.get')
    def test_already_enabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_run, mock_persist):
        """边界：两个参数均已为 1，不执行 sysctl -w 与落盘"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 1\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 1\n"),
        ]

        # Mock test setup.
        S03511_rpacfilter()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Reverse path filtering parameters have already been set to 1...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03511_rpacfilter._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.logger')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display,
                                  mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 0\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 0\n"),
            _run_result(b"", 0),
            _run_result(b"", 0),
            _run_result(b"", 0),
        ]

        # Mock test setup.
        S03511_rpacfilter()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 5)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.all.rp_filter=1"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.default.rp_filter=1"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.route.flush=1"], capture_output=True)
        mock_persist.assert_called_once_with([
            ("net.ipv4.conf.all.rp_filter", "net.ipv4.conf.all.rp_filter=1"),
            ("net.ipv4.conf.default.rp_filter", "net.ipv4.conf.default.rp_filter=1"),
        ])
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Set reverse path filtering parameters to 1...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03511_rpacfilter._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.InsertSection')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.Display')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.logger')
    @patch('secScanner.enhance.euler.set.S03511_rpacfilter.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display,
                        mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result(b"net.ipv4.conf.all.rp_filter = 0\n"),
            _run_result(b"net.ipv4.conf.default.rp_filter = 0\n"),
            _run_result(b"sysctl: permission denied", 1),
            _run_result(b"", 0),
            _run_result(b"", 0),
        ]

        # Mock test setup.
        S03511_rpacfilter()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 5)
        mock_logger.warning.assert_called_once_with("Set reverse path filtering parameters failed")
        mock_Display.assert_called_once_with("- Set reverse path filtering parameters to 1...", "FAILED")


if __name__ == '__main__':
    unittest.main()
