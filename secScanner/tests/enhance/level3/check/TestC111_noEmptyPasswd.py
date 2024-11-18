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
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C111_noEmptyPasswd import C111_noEmptyPasswd

class TestC111_noEmptyPasswd(unittest.TestCase):
    
    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, ""))  # 没有空密码用户
    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.logger')
    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.Display')
    def test_no_empty_password_users(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试函数
        C111_noEmptyPasswd()
        
        # 检查预期的日志信息
        mock_logger.info.assert_called_with("Has no empty password user, checking OK")
        mock_display.assert_called_with("- Check no empty password user...", "OK")

    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(1, ""))  # 有空密码用户
    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.logger')
    @patch('secScanner.enhance.level3.check.C111_noEmptyPasswd.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_password_users_exist(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试函数
        C111_noEmptyPasswd()
        
        # 检查预期的警告信息
        mock_logger.warning.assert_any_call("WRN_C111_01: %s", WRN_C111_01)
        mock_logger.warning.assert_any_call("SUG_C111_01: %s", SUG_C111_01)
        mock_display.assert_called_with("- There is an empty password user present...", "WARNING")

if __name__ == '__main__':
    unittest.main()
