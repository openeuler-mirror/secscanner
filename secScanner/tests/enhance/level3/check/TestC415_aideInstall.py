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
from secScanner.enhance.level3.check.C415_aideInstall import C415_aideInstall

class TestC415_aideInstall(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C415_aideInstall.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, "aide-0.16-14.oe2203sp1.x86_64"))
    @patch('secScanner.enhance.level3.check.C415_aideInstall.logger')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.Display')
    def test_aide_installed_correctly(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C415_aideInstall()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has installed aide correctly, checking ok")
        mock_display.assert_called_with("- Has installed aide correctly ...", "OK")

    @patch('secScanner.enhance.level3.check.C415_aideInstall.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, "package aide is not installed"))
    @patch('secScanner.enhance.level3.check.C415_aideInstall.logger')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_aide_not_installed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C415_aideInstall()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C415: %s", WRN_C415)
        mock_logger.warning.assert_any_call("SUG_C415: %s", SUG_C415)
        mock_display.assert_called_with("- Don't have aide installed...", "WARNING")

if __name__ == '__main__':
    unittest.main()
