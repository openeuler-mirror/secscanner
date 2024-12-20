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
from secScanner.enhance.basic.check.C35_nologinList import C35_nologinList

class TestC35_nologinList(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C35_nologinList.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_listfile.so")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C35_nologinList.logger')
    @patch('secScanner.enhance.basic.check.C35_nologinList.Display')
    def test_login_prohibition_set_correctly(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # 运行测试的函数
        C35_nologinList()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has list of users prohibited from login set, checking OK")
        mock_display.assert_called_with("- Check the list of users prohibited from login...", "OK")

    @patch('secScanner.enhance.basic.check.C35_nologinList.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_listfile.so") 
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.basic.check.C35_nologinList.logger')
    @patch('secScanner.enhance.basic.check.C35_nologinList.Display')
    def test_login_user_deny_file_missing(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # 运行测试的函数
        C35_nologinList()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C35_02: %s", WRN_C35_02)
        mock_logger.warning.assert_any_call("SUG_C35: %s", SUG_C35)
        mock_display.assert_called_with("- No path /etc/login.user.deny...", "WARNING")


    @patch('secScanner.enhance.basic.check.C35_nologinList.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required something.so")
    @patch('os.path.exists', return_value=True)
    @patch('secScanner.enhance.basic.check.C35_nologinList.logger')
    @patch('secScanner.enhance.basic.check.C35_nologinList.Display')
    def test_no_prohibition_config_set(self, mock_display, mock_logger, mock_exists, mock_file, mock_insert):
        # 运行测试的函数
        C35_nologinList()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C35_01: %s", WRN_C35_01)
        mock_logger.warning.assert_any_call("SUG_C35: %s", SUG_C35)
        mock_display.assert_called_with("- No list of users prohibited from login set...", "WARNING")
    
if __name__ == '__main__':
    unittest.main()

