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
from unittest.mock import patch
import logging
from secScanner.enhance.euler.set.S01215_snifftool import S01215_snifftool  # Mock test setup.

class TestS01215_snifftool(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.Display')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.logger')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01215_snifftool()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_snifftool')
        mock_InsertSection.assert_called_once_with("Remove the network sniff tools in your Linux System...")
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set remove the network sniff tools...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.Display')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.logger')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.seconf.get')
    def test_no_tools_installed_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(1, 'package wireshark is not installed'), (1, 'package netcat is not installed'),
                                            (1, 'package tcpdump is not installed'), (1, 'package nmap is not installed'),
                                            (1, 'package ethereal is not installed')]

        # Mock test setup.
        S01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the network sniff tools in your Linux System...")
        sniffTools = ["wireshark", "netcat", "tcpdump", "nmap", "ethereal"]
        for tool in sniffTools:
            mock_getstatusoutput.assert_any_call('rpm -q %s' % tool)
        self.assertEqual(mock_getstatusoutput.call_count, 5)
        mock_logger.info.assert_called_once_with("No package for the network sniff tools")
        mock_Display.assert_called_once_with("- No package for the network sniff tools...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.Display')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.logger')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.seconf.get')
    def test_remove_all_tools_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'wireshark-3.0.0'), (0, 'netcat-1.0'), (0, 'tcpdump-4.9.2'),
                                            (0, 'nmap-7.70'), (0, 'ethereal-1.0'),
                                            (0, ''), (0, ''), (0, ''), (0, ''), (0, '')]

        # Mock test setup.
        S01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the network sniff tools in your Linux System...")
        sniffTools = ["wireshark", "netcat", "tcpdump", "nmap", "ethereal"]
        for tool in sniffTools:
            mock_getstatusoutput.assert_any_call('rpm -q %s' % tool)
            mock_getstatusoutput.assert_any_call('rpm -e %s' % tool)
            mock_logger.info.assert_any_call("Set remove the %s, checking ok" % tool)
        self.assertEqual(mock_getstatusoutput.call_count, 10)
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Set remove the network sniff tools...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01215_snifftool.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.InsertSection')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.Display')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.logger')
    @patch('secScanner.enhance.euler.set.S01215_snifftool.seconf.get')
    def test_partial_tools_remove_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：仅部分工具安装且其中一个卸载失败，应视为 FAILED 并记录失败列表"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(1, 'package wireshark is not installed'), (1, 'package netcat is not installed'),
                                            (0, 'tcpdump-4.9.2'), (0, 'nmap-7.70'),
                                            (1, 'package ethereal is not installed'),
                                            (0, ''), (1, 'error: remove failed')]

        # Mock test setup.
        S01215_snifftool()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the network sniff tools in your Linux System...")
        mock_getstatusoutput.assert_any_call('rpm -e tcpdump')
        mock_getstatusoutput.assert_any_call('rpm -e nmap')
        self.assertEqual(mock_getstatusoutput.call_count, 7)
        mock_logger.warning.assert_any_call("Failed to remove the nmap")
        mock_logger.warning.assert_any_call("Set remove the network sniff tools failed: ['nmap']")
        mock_Display.assert_called_once_with("- Set remove the network sniff tools...", "FAILED")

if __name__ == '__main__':
    unittest.main()
