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
from unittest.mock import patch, mock_open, Mock
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03519_arpproxy import C03519_arpproxy

class TestC03519_arpproxy(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_proxy_arp_enabled_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """不合规：all 与 default 两个参数均非 0，应分别告警并写入 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 1"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 1")]

        secScanner.enhance.euler.check.C03519_arpproxy.RESULT_FILE = "check_result.relt"

        C03519_arpproxy()

        mock_InsertSection.assert_called_once_with("Check whether the ARP proxy is disabled")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['sysctl', 'net.ipv4.conf.all.proxy_arp'], capture_output=True)
        mock_run.assert_any_call(['sysctl', 'net.ipv4.conf.default.proxy_arp'], capture_output=True)
        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_any_call("\nC03519\n")
        mock_logger.warning.assert_any_call("WRN_C03519_0%d: %s", 1, WRN_C03519_01)
        mock_logger.warning.assert_any_call("WRN_C03519_0%d: %s", 2, WRN_C03519_02)
        mock_Display.assert_any_call("- net.ipv4.conf.all.proxy_arp is not set to 0...", "WARNING")
        mock_Display.assert_any_call("- net.ipv4.conf.default.proxy_arp is not set to 0...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_proxy_arp_disabled_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """合规：all 与 default 两个参数均为 0，不写 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 0")]

        C03519_arpproxy()

        mock_InsertSection.assert_called_once_with("Check whether the ARP proxy is disabled")
        mock_file.assert_not_called()
        mock_logger.info.assert_any_call("ARP proxy parameter (%s) is set to 0", "net.ipv4.conf.all.proxy_arp")
        mock_logger.info.assert_any_call("ARP proxy parameter (%s) is set to 0", "net.ipv4.conf.default.proxy_arp")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.all.proxy_arp is set to 0...", "OK")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.default.proxy_arp is set to 0...", "OK")

    @patch('secScanner.enhance.euler.check.C03519_arpproxy.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.InsertSection')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.Display')
    @patch('secScanner.enhance.euler.check.C03519_arpproxy.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_only_default_proxy_arp_enabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：仅 default 参数非 0，应只告警一次、只写入一次 RESULT_FILE"""
        mock_run.side_effect = [Mock(stdout=b"net.ipv4.conf.all.proxy_arp = 0"),
                               Mock(stdout=b"net.ipv4.conf.default.proxy_arp = 1\n")]

        secScanner.enhance.euler.check.C03519_arpproxy.RESULT_FILE = "check_result.relt"

        C03519_arpproxy()

        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03519\n")
        mock_Display.assert_any_call("- Check whether net.ipv4.conf.all.proxy_arp is set to 0...", "OK")
        mock_Display.assert_any_call("- net.ipv4.conf.default.proxy_arp is not set to 0...", "WARNING")

if __name__ == '__main__':
    unittest.main()
