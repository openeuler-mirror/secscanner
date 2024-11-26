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
from secScanner.lib import *
from secScanner.enhance.level3.check.C271_selinux import C271_selinux

class TestC271_selinux(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C271_selinux.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="SELINUX=enforcing\n")
    @patch('secScanner.enhance.level3.check.C271_selinux.logger')
    @patch('secScanner.enhance.level3.check.C271_selinux.Display')
    def test_selinux_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C271_selinux()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has right selinux set, checking ok")
        mock_display.assert_called_with("- Has right selinux set ...", "OK")

    @patch('secScanner.enhance.level3.check.C271_selinux.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="SELINUX=disabled\n")
    @patch('secScanner.enhance.level3.check.C271_selinux.logger')
    @patch('secScanner.enhance.level3.check.C271_selinux.Display')
    def test_selinux_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C271_selinux()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C271: %s", WRN_C271)
        mock_logger.warning.assert_any_call("SUG_C271: %s", SUG_C271)
        mock_display.assert_called_with("- Wrong selinux set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C271_selinux.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C271_selinux.logger')
    @patch('secScanner.enhance.level3.check.C271_selinux.Display')
    def test_config_file_not_exists(self, mock_display, mock_logger, mock_exists, mock_insert):
        # 运行测试的函数
        C271_selinux()

        # 检查文件不存在时的显示信息
        mock_logger.warning.assert_any_call(f"WRN_C271: /etc/selinux/config {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C271: /etc/selinux/config {SUG_no_file}")
        mock_display.assert_called_with("- Config file: /etc/selinux/config not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
