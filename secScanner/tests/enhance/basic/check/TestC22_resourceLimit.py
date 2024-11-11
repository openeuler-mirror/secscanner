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
from secScanner.enhance.basic.check.C22_resourceLimit import C22_resourceLimit

class TestC22_resourceLimit(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.basic.check.C22_resourceLimit.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="* soft core 0\n* hard core 0\n")
    @patch('secScanner.enhance.basic.check.C22_resourceLimit.logger')
    @patch('secScanner.enhance.basic.check.C22_resourceLimit.Display')
    def test_core_limits_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C22_resourceLimit()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_any_call("The system soft core limit is '0, checking ok")
        mock_logger.info.assert_any_call("The system hard core limit is '0, checking ok")
        mock_display.assert_any_call("- Check if the soft core limits is ok...", "OK")
        mock_display.assert_any_call("- Check if the hard core limits is ok...", "OK")

    @patch('secScanner.enhance.basic.check.C22_resourceLimit.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="* soft core 10\n* hard core 10\n")
    @patch('secScanner.enhance.basic.check.C22_resourceLimit.logger')
    @patch('secScanner.enhance.basic.check.C22_resourceLimit.Display')
    def test_core_limits_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C22_resourceLimit()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C22_01: %s", WRN_C22_01)
        mock_logger.warning.assert_any_call("WRN_C22_03: %s", WRN_C22_03)
        mock_display.assert_any_call("- Check if the soft core limits is ok...", "WARNING")
        mock_display.assert_any_call("- Check if the hard core limits is ok...", "WARNING")

if __name__ == '__main__':
    unittest.main()