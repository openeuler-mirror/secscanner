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
from secScanner.enhance.level3.check.C416_chronyInstall import C416_chronyInstall

class TestC416_chronyInstall(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.level3.check.C416_chronyInstall.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'chrony-1.2.3'))
    @patch('secScanner.enhance.level3.check.C416_chronyInstall.logger')
    @patch('secScanner.enhance.level3.check.C416_chronyInstall.Display')
    def test_chrony_installed_correctly(self, mock_display, mock_logger, mock_subproc, mock_insert):
        # 运行测试的函数
        C416_chronyInstall()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has installed chrony correctly, checking ok")
        mock_display.assert_called_with("- Has installed chrony correctly ...", "OK")

    @patch('secScanner.enhance.level3.check.C416_chronyInstall.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'package chrony is not installed'))
    @patch('secScanner.enhance.level3.check.C416_chronyInstall.logger')
    @patch('secScanner.enhance.level3.check.C416_chronyInstall.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_chrony_not_installed(self, mock_file, mock_display, mock_logger, mock_subproc, mock_insert):
        # 运行测试的函数
        C416_chronyInstall()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C416: %s", WRN_C416)
        mock_logger.warning.assert_any_call("SUG_C416: %s", SUG_C416)
        mock_display.assert_called_with("- Don't have chrony installed...", "WARNING")

if __name__ == '__main__':
    unittest.main()
