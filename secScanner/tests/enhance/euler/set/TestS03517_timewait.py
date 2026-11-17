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
from secScanner.enhance.euler.set.S03517_timewait import S03517_timewait

class TestS03517_timewait(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03517_timewait._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.set.S03517_timewait.Display')
    @patch('secScanner.enhance.euler.set.S03517_timewait.logger')
    @patch('secScanner.enhance.euler.set.S03517_timewait.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03517_timewait()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_timewait')
        mock_InsertSection.assert_called_once_with("Set the TIME WAIT tcp fin timeout not greater than 60...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set net.ipv4.tcp_fin_timeout due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03517_timewait._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.set.S03517_timewait.Display')
    @patch('secScanner.enhance.euler.set.S03517_timewait.logger')
    @patch('secScanner.enhance.euler.set.S03517_timewait.seconf.get')
    def test_already_right_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """边界：配置开启但 tcp_fin_timeout 已等于 60，无需再次设置"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 60\n", returncode=0)

        # Mock test setup.
        S03517_timewait()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_timewait')
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.tcp_fin_timeout'], capture_output=True)
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- net.ipv4.tcp_fin_timeout has already been set to 60...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03517_timewait._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.set.S03517_timewait.Display')
    @patch('secScanner.enhance.euler.set.S03517_timewait.logger')
    @patch('secScanner.enhance.euler.set.S03517_timewait.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 120\n", returncode=0),
            MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 60\n", returncode=0)
        ]

        # Mock test setup.
        S03517_timewait()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_timewait')
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['sysctl', '-w', 'net.ipv4.tcp_fin_timeout=60'], capture_output=True)
        mock_persist.assert_called_once_with([('net.ipv4.tcp_fin_timeout', 'net.ipv4.tcp_fin_timeout=60')])
        mock_logger.info.assert_any_call("Set %s finish", 'net.ipv4.tcp_fin_timeout')
        mock_Display.assert_called_once_with("- Set net.ipv4.tcp_fin_timeout=60...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03517_timewait._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.set.S03517_timewait.Display')
    @patch('secScanner.enhance.euler.set.S03517_timewait.logger')
    @patch('secScanner.enhance.euler.set.S03517_timewait.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [
            MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 120\n", returncode=0),
            MagicMock(stdout=b"", returncode=1)
        ]

        # Mock test setup.
        S03517_timewait()

        # Mock test setup.
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.warning.assert_called_once_with("Set %s failed", 'net.ipv4.tcp_fin_timeout')
        mock_Display.assert_called_once_with("- Set net.ipv4.tcp_fin_timeout=60...", "FAILED")

if __name__ == '__main__':
    unittest.main()
