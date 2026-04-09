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
from secScanner.lib.textInfo_euler import WRN_no_file, SUG_no_file
from secScanner.enhance.level3.check.C415_aideInstall import C415_aideInstall

class TestC415_aideInstall(unittest.TestCase):

    @patch('subprocess.getstatusoutput', return_value=(0, 'aide-0.16.1-10.el8.x86_64'))
    @patch('secScanner.enhance.level3.check.C415_aideInstall.InsertSection')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.Display')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.logger')
    def test_aide_installed(self, mock_logger, mock_display, mock_insert, mock_subprocess):
        # 调用被测试函数
        C415_aideInstall()

        # 验证函数行为
        mock_logger.info.assert_called_with("Has installed aide correctly, checking ok")
        mock_display.assert_called_with("- Has installed aide correctly ...", "OK")


    @patch('subprocess.getstatusoutput', return_value=(2, 'error message'))
    @patch('secScanner.enhance.level3.check.C415_aideInstall.InsertSection')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.Display')
    @patch('secScanner.enhance.level3.check.C415_aideInstall.logger')
    def test_aide_check_failed(self, mock_logger, mock_display, mock_insert, mock_subprocess):
        # 调用被测试函数
        C415_aideInstall()

        # 验证函数行为
        mock_logger.error.assert_called_with("check the aide status failed")
        mock_display.assert_called_with("- Error occured while checking aide status...", "FAILED")

if __name__ == "__main__":
    unittest.main()
