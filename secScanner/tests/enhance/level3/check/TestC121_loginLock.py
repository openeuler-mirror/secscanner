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
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_level3 import *
from secScanner.lib.textInfo_basic import *
from secScanner.lib.textInfo_euler import WRN_no_file, SUG_no_file
from secScanner.enhance.level3.check.C121_loginLock import C121_loginLock

class TestC121_loginLock(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C121_loginLock.get_value')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_faillock.so deny=3 unlock_time=300")
    @patch('secScanner.enhance.level3.check.C121_loginLock.InsertSection')
    @patch('secScanner.enhance.level3.check.C121_loginLock.Display')
    @patch('secScanner.enhance.level3.check.C121_loginLock.logger')
    def test_login_lock_correct(self, mock_logger, mock_display, mock_insert, mock_file, mock_get_value):
        # 模拟系统信息
        mock_get_value.side_effect = lambda x: {"OS_ID": "centos", "OS_DISTRO": "8"}[x]

        # 调用被测试函数
        C121_loginLock()

        # 验证函数行为
        mock_logger.info.assert_called_with("Has user login lock Deny set, checking OK")
        mock_display.assert_called_with("- Has user login lock Deny set...", "OK")

    @patch('secScanner.enhance.level3.check.C121_loginLock.get_value')
    @patch('builtins.open', new_callable=mock_open, read_data="auth required pam_faillock.so deny=6 unlock_time=300")
    @patch('secScanner.enhance.level3.check.C121_loginLock.InsertSection')
    @patch('secScanner.enhance.level3.check.C121_loginLock.Display')
    @patch('secScanner.enhance.level3.check.C121_loginLock.logger')
    def test_login_lock_incorrect(self, mock_logger, mock_display, mock_insert, mock_file, mock_get_value):
        # 模拟系统信息
        mock_get_value.side_effect = lambda x: {"OS_ID": "centos", "OS_DISTRO": "8"}[x]

        # 调用被测试函数
        C121_loginLock()

        # 验证函数行为
        mock_logger.warning.assert_any_call("WRN_C121_01: %s", WRN_C04_01)
        mock_logger.warning.assert_any_call("SUG_C121: %s", SUG_C04)
        mock_display.assert_called_with("- Wrong user login lock Deny set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C121_loginLock.get_value')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.level3.check.C121_loginLock.InsertSection')
    @patch('secScanner.enhance.level3.check.C121_loginLock.Display')
    @patch('secScanner.enhance.level3.check.C121_loginLock.logger')
    def test_login_lock_not_set(self, mock_logger, mock_display, mock_insert, mock_file, mock_get_value):
        # 模拟系统信息
        mock_get_value.side_effect = lambda x: {"OS_ID": "centos", "OS_DISTRO": "8"}[x]

        # 调用被测试函数
        C121_loginLock()

        # 验证函数行为
        mock_logger.warning.assert_any_call("WRN_C121_02: %s", WRN_C04_02)
        mock_logger.warning.assert_any_call("SUG_C121: %s", SUG_C04)
        mock_display.assert_called_with("- No user login lock Deny set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C121_loginLock.get_value')
    @patch('secScanner.enhance.level3.check.C121_loginLock.InsertSection')
    @patch('secScanner.enhance.level3.check.C121_loginLock.Display')
    @patch('secScanner.enhance.level3.check.C121_loginLock.logger')
    def test_unsupported_os(self, mock_logger, mock_display, mock_insert, mock_get_value):
        # 模拟系统信息
        mock_get_value.side_effect = lambda x: {"OS_ID": "ubuntu", "OS_DISTRO": "20.04"}[x]

        # 调用被测试函数
        C121_loginLock()

        # 验证函数行为
        mock_logger.warning.assert_called_with("We do not support ubuntu-20.04 at this moment")
        mock_display.assert_called_with("- We do not support ubuntu-20.04 at this moment...", "WARNING")

if __name__ == "__main__":
    unittest.main()
