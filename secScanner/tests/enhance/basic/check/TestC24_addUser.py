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
from secScanner.enhance.basic.check.C24_addUser import C24_addUser

class TestC24_addUser(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.basic.check.C24_addUser.InsertSection')
    @patch('secScanner.enhance.basic.check.C24_addUser.seconf.options', return_value=['username'])
    @patch('secScanner.enhance.basic.check.C24_addUser.seconf.get', return_value='testuser')
    @patch('builtins.open', new_callable=mock_open, read_data="root:x:0:0:root:/root:/bin/bash\ntestuser:x:1001:1001::/home/testuser:/bin/bash\n")
    @patch('secScanner.enhance.basic.check.C24_addUser.logger')
    @patch('secScanner.enhance.basic.check.C24_addUser.Display')
    def test_user_exists(self, mock_display, mock_logger, mock_file, mock_get, mock_options, mock_insert):
        # 运行测试的函数
        C24_addUser()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Already have testuser, no need to add")
        mock_display.assert_called_with("- Already have testuser...", "OK")

    @patch('secScanner.enhance.basic.check.C24_addUser.InsertSection')
    @patch('secScanner.enhance.basic.check.C24_addUser.seconf.options', return_value=['username'])
    @patch('secScanner.enhance.basic.check.C24_addUser.seconf.get', return_value='newuser')
    @patch('builtins.open', new_callable=mock_open, read_data="root:x:0:0:root:/root:/bin/bash\ntestuser:x:1001:1001::/home/testuser:/bin/bash\n")
    @patch('secScanner.enhance.basic.check.C24_addUser.logger')
    @patch('secScanner.enhance.basic.check.C24_addUser.Display')
    def test_user_not_exists(self, mock_display, mock_logger, mock_file, mock_get, mock_options, mock_insert):
        # 运行测试的函数
        C24_addUser()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C24: %s", WRN_C24)
        mock_display.assert_called_with("- No additional user found, check warning", "WARNING")

if __name__ == '__main__':
    unittest.main()
