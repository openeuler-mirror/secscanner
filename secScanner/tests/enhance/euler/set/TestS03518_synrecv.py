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
from secScanner.enhance.euler.set.S03518_synrecv import S03518_synrecv

class TestS03518_synrecv(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03518_synrecv._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.Display')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.logger')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """配置为 no，应跳过设置"""
        mock_seconf_get.return_value = 'no'

        S03518_synrecv()

        mock_seconf_get.assert_called_once_with('euler', 'set_synrecv')
        mock_InsertSection.assert_called_once_with("Set the SYN_RECV state queue number to 256...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set net.ipv4.tcp_max_syn_backlog due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03518_synrecv._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.Display')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.logger')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """设置成功，应持久化配置并输出 FINISHED"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 128"),
                               Mock(returncode=0)]

        S03518_synrecv()

        mock_seconf_get.assert_called_once_with('euler', 'set_synrecv')
        mock_InsertSection.assert_called_once_with("Set the SYN_RECV state queue number to 256...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['sysctl', 'net.ipv4.tcp_max_syn_backlog'], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.tcp_max_syn_backlog=256"], capture_output=True)
        mock_persist.assert_called_once_with([("net.ipv4.tcp_max_syn_backlog", "net.ipv4.tcp_max_syn_backlog=256")])
        mock_logger.info.assert_any_call("Set %s finish", "net.ipv4.tcp_max_syn_backlog")
        mock_Display.assert_called_once_with("- Set net.ipv4.tcp_max_syn_backlog=256...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03518_synrecv._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.Display')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.logger')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """sysctl -w 返回非 0，应输出 FAILED 且不持久化配置"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 128"),
                               Mock(returncode=1)]

        S03518_synrecv()

        mock_InsertSection.assert_called_once_with("Set the SYN_RECV state queue number to 256...")
        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_logger.warning.assert_called_once_with("Set %s failed", "net.ipv4.tcp_max_syn_backlog")
        mock_Display.assert_called_once_with("- Set net.ipv4.tcp_max_syn_backlog=256...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03518_synrecv._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.Display')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.logger')
    @patch('secScanner.enhance.euler.set.S03518_synrecv.seconf.get')
    def test_already_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """边界：当前值已不小于 256，无需重复设置"""
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 256")

        S03518_synrecv()

        self.assertEqual(mock_run.call_count, 1)
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.tcp_max_syn_backlog'], capture_output=True)
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- net.ipv4.tcp_max_syn_backlog has already been set to 256...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
