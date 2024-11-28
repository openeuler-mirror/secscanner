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
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C422_DNSserver import C422_DNSserver

class TestC422_DNSserver(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C422_DNSserver.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'enabled'))
    @patch('secScanner.enhance.level3.check.C422_DNSserver.logger')
    @patch('secScanner.enhance.level3.check.C422_DNSserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_dns_server_enabled(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C422_DNSserver()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C422: %s", WRN_C422)
        mock_logger.warning.assert_any_call("SUG_C422: %s", SUG_C422)
        mock_display.assert_called_with("- Check the DNS-Server is enabled ...", "WARNING")

    @patch('secScanner.enhance.level3.check.C422_DNSserver.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C422_DNSserver.logger')
    @patch('secScanner.enhance.level3.check.C422_DNSserver.Display')
    def test_dns_server_disabled(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C422_DNSserver()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("The DNS-Server status is: disabled")
        mock_display.assert_called_with("- Check the DNS-Server is disabled...", "OK")

if __name__ == '__main__':
    unittest.main()
