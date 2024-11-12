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


import subprocess
import unittest
from unittest.mock import patch, mock_open
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0201_lockUnUsedUser import C0201_lockUnUsedUser

class TestC0201_lockUnUsedUser(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.InsertSection')
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.seconf.get', return_value='adm lp')
    @patch('subprocess.check_output', side_effect=[
        b"adm::::::::",
        b"lp::12345::::::"
    ])
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.logger')
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.Display')
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.open')
    def test_some_users_unlocked(self, mock_open, mock_display, mock_logger, mock_subproc, mock_config, mock_insert):
        # 运行测试的函数
        C0201_lockUnUsedUser()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C0201: These users: ['adm', 'lp'] should lock")
        mock_logger.warning.assert_any_call("SUG_C0201: %s", SUG_C0201)
        mock_display.assert_any_call("- Check if there have unused user...", "WARNING")

    
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.InsertSection')
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.seconf.get', return_value='adm lp')
    @patch('subprocess.check_output', side_effect=[
        b"adm:!*:12345::::::",
        b"lp:!*:12345::::::"
    ])
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.logger')
    @patch('secScanner.enhance.euler.check.C0201_lockUnUsedUser.Display')
    def test_all_users_locked(self, mock_display, mock_logger, mock_subproc, mock_config, mock_insert):
        # 运行测试的函数
        C0201_lockUnUsedUser()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("All unused user is locked, checking ok")
        mock_display.assert_called_with("- Check if there have unused user...", "OK")

if __name__ == '__main__':
    unittest.main()

