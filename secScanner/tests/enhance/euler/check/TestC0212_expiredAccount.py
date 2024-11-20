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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0212_expiredAccount import C0212_expiredAccount
import secScanner

class TestC0212_expiredAccount(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='user1:$6$hash:17597:0:99999:7:::\nuser2:$6$hash:17597:0:99999:7::17000\n')
    @patch('enhance.euler.check.C0212_expiredAccount.datetime')
    def test_expired_account_exists(self, mock_datetime, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟存在过期账户
        mock_exists.return_value = True
        mock_datetime.datetime.now.timestamp.return_value = 1730684465
        secScanner.enhance.euler.check.C0212_expiredAccount.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0212_expiredAccount()
        mock_InsertSection.assert_any_call("check for expired account")
        mock_logger.warning.assert_any_call("WRN_C0212_01: %s", WRN_C0212_01)
        mock_logger.warning.assert_any_call("SUG_C0212_01: %s", SUG_C0212_01)
        mock_display.assert_called_once_with("- At least one account has expired", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='user1:$6$hash:17597:0:99999:7:::\nuser2:$6$hash:17597:0:99999:7:::\n')
    @patch('enhance.euler.check.C0212_expiredAccount.datetime')
    def test_no_expired_accounts(self, mock_datetime, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟不存在过期账户
        mock_exists.return_value = True
        mock_datetime.datetime.now.timestamp.return_value = 1730684465

        # 调用测试函数
        C0212_expiredAccount()
        mock_InsertSection.assert_any_call("check for expired account")
        mock_logger.info.assert_any_call('No expired account exists, checking ok')
        mock_display.assert_called_once_with("- No expired account exists", "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.logger')
    @patch('secScanner.enhance.euler.check.C0212_expiredAccount.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_shadow_file_not_exists(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_exists):
        # 模拟/etc/shadow文件不存在
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0212_expiredAccount.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0212_expiredAccount()
        mock_InsertSection.assert_any_call("check for expired account")
        mock_logger.warning.assert_any_call("WRN_C0212_02: %s", WRN_C0212_02)
        mock_logger.warning.assert_any_call("SUG_C0212_02: %s", SUG_C0212_02)
        mock_display.assert_called_once_with("- file /etc/shadow dose not exist...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()