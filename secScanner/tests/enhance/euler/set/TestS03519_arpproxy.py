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
from secScanner.enhance.euler.set.S03519_arpproxy import S03519_arpproxy

class TestS03519_arpproxy(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03519_arpproxy._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.logger')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """配置为 no，应跳过设置"""
        mock_seconf_get.return_value = 'no'

        S03519_arpproxy()

        mock_seconf_get.assert_called_once_with('euler', 'set_arpproxy')
        mock_InsertSection.assert_called_once_with("Set the ARP proxy disabled...")
        mock_run.assert_not_called()
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set ARP proxy parameters due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03519_arpproxy._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.logger')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.seconf.get')
    def test_set_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """两个参数均需设置且全部成功，应持久化配置并输出 FINISHED"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 1"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 1"),
                               Mock(returncode=0),
                               Mock(returncode=0)]

        S03519_arpproxy()

        mock_seconf_get.assert_called_once_with('euler', 'set_arpproxy')
        mock_InsertSection.assert_called_once_with("Set the ARP proxy disabled...")
        self.assertEqual(mock_run.call_count, 4)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.all.proxy_arp=0"], capture_output=True)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.default.proxy_arp=0"], capture_output=True)
        mock_persist.assert_called_once_with([("net.ipv4.conf.all.proxy_arp", "net.ipv4.conf.all.proxy_arp=0"),
                                              ("net.ipv4.conf.default.proxy_arp", "net.ipv4.conf.default.proxy_arp=0")])
        mock_logger.info.assert_any_call("Set ARP proxy parameters finish")
        mock_Display.assert_called_once_with("- Set ARP proxy parameters to 0...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03519_arpproxy._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.logger')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.seconf.get')
    def test_set_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """sysctl -w 返回非 0，应输出 FAILED"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 1"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 0"),
                               Mock(returncode=1)]

        S03519_arpproxy()

        mock_InsertSection.assert_called_once_with("Set the ARP proxy disabled...")
        self.assertEqual(mock_run.call_count, 3)
        mock_run.assert_any_call(["sysctl", "-w", "net.ipv4.conf.all.proxy_arp=0"], capture_output=True)
        mock_logger.warning.assert_called_once_with("Set ARP proxy parameters failed")
        mock_Display.assert_called_once_with("- Set ARP proxy parameters to 0...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03519_arpproxy._persist_sysctl')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.logger')
    @patch('secScanner.enhance.euler.set.S03519_arpproxy.seconf.get')
    def test_already_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_persist):
        """边界：两个参数均已为 0，无需重复设置"""
        mock_seconf_get.return_value = 'yes'
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 0")]

        S03519_arpproxy()

        self.assertEqual(mock_run.call_count, 2)
        mock_persist.assert_not_called()
        mock_Display.assert_called_once_with("- ARP proxy parameters have already been set to 0...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
