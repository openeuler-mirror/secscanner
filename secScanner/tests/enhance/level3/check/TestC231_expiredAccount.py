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
from secScanner.enhance.level3.check.C231_expiredAccount import C231_expiredAccount

class TestC231_expiredAccount(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()

    @patch('secScanner.enhance.level3.check.C231_expiredAccount.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="user1:x:1000:1000::/home/user1:/bin/bash:99999\nuser2:x:1001:1001::/home/user2:/bin/bash:99999\n")
    @patch('secScanner.enhance.level3.check.C231_expiredAccount.logger')
    @patch('secScanner.enhance.level3.check.C231_expiredAccount.Display')
    def test_no_expired_accounts(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C231_expiredAccount()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with('No expired account exists, checking ok')
        mock_display.assert_called_with("- No expired account exists", "OK")

    @patch('secScanner.enhance.level3.check.C231_expiredAccount.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="user1:x:1000:1000::/home/user1:/bin/bash:1\nuser2:x:1001:1001::/home/user2:/bin/bash:1\n")
    @patch('secScanner.enhance.level3.check.C231_expiredAccount.logger')
    @patch('secScanner.enhance.level3.check.C231_expiredAccount.Display')
    def test_expired_accounts_exist(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C231_expiredAccount()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C231_01: %s", WRN_C231_01)
        mock_logger.warning.assert_any_call("SUG_C231_01: %s", SUG_C231_01)
        mock_display.assert_called_with("- At least one account has expired", "WARNING")

if __name__ == '__main__':
    unittest.main()
