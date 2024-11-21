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
from secScanner.commands.check_outprint import *
from secScanner.enhance.level3.check.C221_sshRootDenie import C221_sshRootDenie

# 定义测试类
class TestC221_sshRootDenie(unittest.TestCase):
    def setUp(self):
        # 设置模拟函数get_value返回的值
        self.os_distro = '7'

    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.get_value', return_value='7')
    @patch('builtins.open', new_callable=mock_open, read_data="pts/0\npts/1\n")
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.Display')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.logger')
    def test_securetty_wrong_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        # 运行测试的函数
        C221_sshRootDenie()
        
        # 检查预期的警告信息是否已正确显示
        mock_display.assert_any_call("- Wrong Telnet Denie set...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C221_01: %s", WRN_C221_01)
        mock_logger.warning.assert_any_call("SUG_C221: %s", SUG_C221)
        mock_display.assert_any_call("- No ssh Root denie set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.get_value', return_value='7')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.Display')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.logger')
    def test_securetty_correct_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        # 运行测试的函数
        C221_sshRootDenie()

        # 检查预期的OK信息是否已正确显示
        mock_display.assert_any_call("- Check the telnet deny...", "OK")
        mock_logger.warning.assert_any_call("WRN_C221_01: %s", WRN_C221_01)
        mock_logger.warning.assert_any_call("SUG_C221: %s", SUG_C221)
        mock_display.assert_any_call("- No ssh Root denie set...", "WARNING")
    
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.get_value', return_value='any_other_value')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin no\n")
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.Display')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.logger')
    def test_ssh_config_right_setting(self, mock_logger, mock_display, mock_file, mock_get_value, mock_insert):
        # 运行测试的函数
        C221_sshRootDenie()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_any_call("Has ssh Root denie set, checking OK")
        mock_display.assert_any_call("- Check the ssh Root denie...", "OK")

    
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.InsertSection')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.get_value', return_value='any_other_value')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin yes\n")
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.logger')
    @patch('secScanner.enhance.level3.check.C221_sshRootDenie.Display')
    def test_ssh_config_wrong_setting(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        # 运行测试的函数
        C221_sshRootDenie()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C221_02: %s", WRN_C221_02)
        mock_logger.warning.assert_any_call("SUG_C221: %s", SUG_C221) 
        mock_display.assert_any_call("- Wrong ssh Root denie set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

