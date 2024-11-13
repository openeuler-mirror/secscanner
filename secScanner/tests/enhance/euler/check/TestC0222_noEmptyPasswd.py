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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0222_noEmptyPasswd import C0222_noEmptyPasswd

class TestC0222_noEmptyPasswd(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitEmptyPasswords no\n")
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.logger')
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.Display')
    def test_permit_empty_passwords_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C0222_noEmptyPasswd()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ssh PermitEmptyPasswords set, checking OK")
        mock_display.assert_called_with("- Check the ssh PermitEmptyPasswords...", "OK")

    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitEmptyPasswords yes\n")
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.logger')
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.Display')
    def test_permit_empty_passwords_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C0222_noEmptyPasswd()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C0222_02: %s", WRN_C0222_02)
        mock_logger.warning.assert_any_call("SUG_C0222_02: %s", SUG_C0222_02)
        mock_display.assert_called_with("- Wrong ssh PermitEmptyPasswords config set...", "WARNING")

    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.logger')
    @patch('secScanner.enhance.euler.check.C0222_noEmptyPasswd.Display')
    def test_no_permit_empty_passwords_set(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C0222_noEmptyPasswd()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C0222_01: %s", WRN_C0222_01)
        mock_logger.warning.assert_any_call("SUG_C0222_01: %s", SUG_C0222_01)
        mock_display.assert_called_with("- No ssh PermitEmptyPasswords config set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

