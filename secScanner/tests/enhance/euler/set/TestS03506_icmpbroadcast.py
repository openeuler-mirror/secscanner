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
from secScanner.enhance.euler.set.S03506_icmpbroadcast import S03506_icmpbroadcast  # Mock test setup.

SYSCTL_CMD = ['sysctl', 'net.ipv4.icmp_echo_ignore_broadcasts']
SET_CMD = ["sysctl", "-w", "net.ipv4.icmp_echo_ignore_broadcasts=1"]


def _sysctl_result(stdout, returncode=0):
    result = MagicMock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestS03506_icmpbroadcast(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.InsertSection')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03506_icmpbroadcast()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_icmpbroadcast')
        mock_InsertSection.assert_called_once_with("Set the system not to respond ICMP broadcast packets...")
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set net.ipv4.icmp_echo_ignore_broadcasts due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.InsertSection')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                  mock_run, mock_persist_sysctl):
        """配置为 yes 且当前值为 0，设置成功应 FINISHED 并持久化"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [_sysctl_result(b"net.ipv4.icmp_echo_ignore_broadcasts = 0\n"),
                                _sysctl_result(b"", 0)]

        # Mock test setup.
        S03506_icmpbroadcast()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_icmpbroadcast')
        mock_InsertSection.assert_called_once_with("Set the system not to respond ICMP broadcast packets...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(SYSCTL_CMD, capture_output=True)
        mock_run.assert_any_call(SET_CMD, capture_output=True)
        mock_persist_sysctl.assert_called_once_with(
            [("net.ipv4.icmp_echo_ignore_broadcasts", "net.ipv4.icmp_echo_ignore_broadcasts=1")])
        mock_logger.info.assert_any_call("Set net.ipv4.icmp_echo_ignore_broadcasts finish")
        mock_Display.assert_called_once_with("- Set net.ipv4.icmp_echo_ignore_broadcasts=1...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.InsertSection')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                        mock_run, mock_persist_sysctl):
        """配置为 yes 但设置命令返回非 0，应 FAILED 且不持久化"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [_sysctl_result(b"net.ipv4.icmp_echo_ignore_broadcasts = 0\n"),
                                _sysctl_result(b"", 1)]

        # Mock test setup.
        S03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the system not to respond ICMP broadcast packets...")
        self.assertEqual(mock_run.call_count, 2)
        mock_persist_sysctl.assert_not_called()
        mock_logger.warning.assert_called_once_with("Set net.ipv4.icmp_echo_ignore_broadcasts failed")
        mock_Display.assert_called_once_with("- Set net.ipv4.icmp_echo_ignore_broadcasts=1...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.logger')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.Display')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.InsertSection')
    @patch('secScanner.enhance.euler.set.S03506_icmpbroadcast.seconf.get')
    def test_already_ignored_skipping(self, mock_seconf_get, mock_InsertSection, mock_Display, mock_logger,
                                      mock_run, mock_persist_sysctl):
        """边界：当前值已为 1 时不做设置，直接 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [_sysctl_result(b"net.ipv4.icmp_echo_ignore_broadcasts = 1\n")]

        # Mock test setup.
        S03506_icmpbroadcast()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the system not to respond ICMP broadcast packets...")
        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_once_with(SYSCTL_CMD, capture_output=True)
        mock_persist_sysctl.assert_not_called()
        mock_logger.info.assert_called_once_with("net.ipv4.icmp_echo_ignore_broadcasts already set to 1")
        mock_Display.assert_called_once_with("- net.ipv4.icmp_echo_ignore_broadcasts has already been set to 1...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
