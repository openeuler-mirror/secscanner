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
from secScanner.enhance.euler.set.S03515_spooflog import S03515_spooflog

class TestS03515_spooflog(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03515_spooflog._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.Display')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.logger')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """配置为 no，应跳过设置"""
        mock_seconf_get.return_value = 'no'

        S03515_spooflog()

        mock_seconf_get.assert_called_once_with('euler', 'set_spooflog')
        mock_InsertSection.assert_called_once_with("Set the spoofing, source-routed and redirect packets logged...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set log martians parameters due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03515_spooflog._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.Display')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.logger')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.seconf.get')
    def test_already_enabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """边界：两个参数均已为 1，无需重复设置"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 1"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 1")]

        S03515_spooflog()

        mock_InsertSection.assert_called_once_with("Set the spoofing, source-routed and redirect packets logged...")
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.info.assert_called_once_with("Log martians parameters already set to 1")
        mock_Display.assert_called_once_with("- Log martians parameters have already been set to 1...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03515_spooflog._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.Display')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.logger')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """两个参数均需设置且成功，应持久化配置并输出 FINISHED"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 0"),
                               Mock(returncode=0),
                               Mock(returncode=0)]

        S03515_spooflog()

        mock_InsertSection.assert_called_once_with("Set the spoofing, source-routed and redirect packets logged...")
        self.assertEqual(mock_run.call_count, 4)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.all.log_martians=1"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.default.log_martians=1"], capture_output=True)
        mock_persist.assert_called_once_with([("net.ipv4.conf.all.log_martians", "net.ipv4.conf.all.log_martians=1"),
                                             ("net.ipv4.conf.default.log_martians", "net.ipv4.conf.default.log_martians=1")])
        mock_logger.info.assert_any_call("Set log martians parameters finish")
        mock_Display.assert_called_once_with("- Set log martians parameters to 1...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03515_spooflog._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.InsertSection')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.Display')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.logger')
    @patch('secScanner.enhance.euler.set.S03515_spooflog.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """sysctl -w 返回非 0，应输出 FAILED"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.log_martians = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.log_martians = 0"),
                               Mock(returncode=1),
                               Mock(returncode=0)]

        S03515_spooflog()

        mock_InsertSection.assert_called_once_with("Set the spoofing, source-routed and redirect packets logged...")
        self.assertEqual(mock_run.call_count, 4)
        mock_logger.warning.assert_called_once_with("Set log martians parameters failed")
        mock_Display.assert_called_once_with("- Set log martians parameters to 1...", "FAILED")

if __name__ == '__main__':
    unittest.main()
