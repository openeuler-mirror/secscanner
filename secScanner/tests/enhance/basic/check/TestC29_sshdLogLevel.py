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
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C29_sshdLogLevel import C29_sshdLogLevel

class TestC29_sshdLogLevel(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="LogLevel VERBOSE\n")
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.logger')
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.Display')
    def test_loglevel_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C29_sshdLogLevel()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ssh loglevel set, checking OK")
        mock_display.assert_called_with("- Check the ssh loglevel...", "OK")

    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="LogLevel INFO\n")
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.logger')
    @patch('secScanner.enhance.basic.check.C29_sshdLogLevel.Display')
    def test_loglevel_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C29_sshdLogLevel()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C29_02: %s", WRN_C29_02)
        mock_logger.warning.assert_any_call("SUG_C29: %s", SUG_C29)
        mock_display.assert_called_with("- Wrong ssh loglevel config set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

