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
from unittest.mock import patch, mock_open
import secScanner
from secScanner.lib.textInfo_basic import *

class TestC05_icmpLimit(unittest.TestCase):
    def setUp(self):
        # 正确配置的文件内容
        self.sysctl_conf_correct = "net.ipv4.conf.all.accept_redirects=0\n"
        # 错误或缺失配置的文件内容
        self.sysctl_conf_incorrect = "# net.ipv4.conf.all.accept_redirects=0\n"

    @patch("secScanner.enhance.basic.check.C05_icmpLimit.InsertSection")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.open", new_callable=mock_open, read_data="net.ipv4.conf.all.accept_redirects=0\n")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.logger")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.Display")
    def test_icmpLimit_correct_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.basic.check.C05_icmpLimit.C05_icmpLimit()
        mock_logger.info.assert_called_with("Has icmp redirect limit set, checking ok")
        mock_display.assert_called_with("- Has icmp redirect limit set...", "OK")

    @patch("secScanner.enhance.basic.check.C05_icmpLimit.InsertSection")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.open", new_callable=mock_open, read_data="# net.ipv4.conf.all.accept_redirects=0\n")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.logger")
    @patch("secScanner.enhance.basic.check.C05_icmpLimit.Display")
    def test_icmpLimit_incorrect_setting(self, mock_display, mock_logger, mock_file, mock_insert):
        secScanner.enhance.basic.check.C05_icmpLimit.C05_icmpLimit()
        mock_logger.warning.assert_any_call("WRN_C05: %s", WRN_C05)
        mock_logger.warning.assert_any_call("SUG_C05: %s", SUG_C05)
        mock_display.assert_called_with("- Wrong icmp limit set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

