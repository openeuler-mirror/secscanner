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
from secScanner.enhance.level3.check.C241_noOneSU import C241_noOneSU

class TestC241_noOneSU(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.level3.check.C241_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_wheel.so group=wheel\n")
    @patch('secScanner.enhance.level3.check.C241_noOneSU.logger')
    @patch('secScanner.enhance.level3.check.C241_noOneSU.Display')
    def test_pam_wheel_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C241_noOneSU()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("There have pam_wheel set, check OK")
        mock_display.assert_called_with("- Check the pam.d/su setting...", "OK")

    @patch('secScanner.enhance.level3.check.C241_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_unix.so\n")
    @patch('secScanner.enhance.level3.check.C241_noOneSU.logger')
    @patch('secScanner.enhance.level3.check.C241_noOneSU.Display')
    def test_pam_wheel_not_set(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C241_noOneSU()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C241: %s", WRN_C241)
        mock_display.assert_called_with("- There is no pam_wheel set, check warning", "WARNING")

    @patch('secScanner.enhance.level3.check.C241_noOneSU.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.level3.check.C241_noOneSU.logger')
    @patch('secScanner.enhance.level3.check.C241_noOneSU.Display')
    def test_pam_file_empty(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C241_noOneSU()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C241: %s", WRN_C241)
        mock_display.assert_called_with("- There is no pam_wheel set, check warning", "WARNING")

if __name__ == '__main__':
    unittest.main()

