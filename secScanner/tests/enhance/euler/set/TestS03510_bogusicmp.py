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
from secScanner.enhance.euler.set.S03510_bogusicmp import S03510_bogusicmp  # Mock test setup.

PARAM = "net.ipv4.icmp_ignore_bogus_error_responses"


def _run_result(stdout=b"", returncode=0):
    result = Mock()
    result.stdout = stdout
    result.returncode = returncode
    return result


class TestS03510_bogusicmp(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03510_bogusicmp._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.logger')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03510_bogusicmp()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_bogusicmp')
        mock_InsertSection.assert_called_once_with("Set the system to ignore bogus ICMP error responses...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with(
            "- Skip set net.ipv4.icmp_ignore_bogus_error_responses due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03510_bogusicmp._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.logger')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.seconf.get')
    def test_already_enabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_run, mock_persist):
        """边界：参数已为 1，不再执行 sysctl -w"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 1\n")

        # Mock test setup.
        S03510_bogusicmp()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_bogusicmp')
        mock_InsertSection.assert_called_once_with("Set the system to ignore bogus ICMP error responses...")
        mock_run.assert_called_once_with(['sysctl', PARAM], capture_output=True)
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- %s has already been set to 1..." % PARAM, "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03510_bogusicmp._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.logger')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display,
                                  mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 0\n"),
            _run_result(b"", 0),
            _run_result(b"", 0),
        ]

        # Mock test setup.
        S03510_bogusicmp()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 3)
        mock_run.assert_any_call(['sysctl', PARAM], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "%s=1" % PARAM], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.route.flush=1"], capture_output=True)
        mock_persist.assert_called_once_with([(PARAM, "%s=1" % PARAM)])
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Set %s=1..." % PARAM, "FINISHED")

    @patch('secScanner.enhance.euler.set.S03510_bogusicmp._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.InsertSection')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.Display')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.logger')
    @patch('secScanner.enhance.euler.set.S03510_bogusicmp.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display,
                        mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            _run_result(b"net.ipv4.icmp_ignore_bogus_error_responses = 0\n"),
            _run_result(b"sysctl: permission denied", 1),
        ]

        # Mock test setup.
        S03510_bogusicmp()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.warning.assert_called_once_with("Set %s failed", PARAM)
        mock_Display.assert_called_once_with("- Set %s=1..." % PARAM, "FAILED")


if __name__ == '__main__':
    unittest.main()
