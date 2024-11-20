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
from secScanner.enhance.euler.check.C0228_warnBanner import C0228_warnBanner
import secScanner

class TestC0228_warnBanner(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.InsertSection')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.logger')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.getsize')
    def test_all_files_exist(self, mock_getsize, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟所有文件都存在且有内容
        mock_exists.side_effect = lambda x: True
        mock_getsize.side_effect = lambda x: 100
        # 调用测试函数
        C0228_warnBanner()

        mock_InsertSection.assert_any_call("check system warning  banner")
        mock_logger.info.assert_any_call("Has /etc/motd set, checking ok")
        mock_display.assert_any_call("- Has /etc/motd warning banner...",  "OK")
        mock_logger.info.assert_any_call("Has /etc/issue set, checking ok")
        mock_display.assert_any_call("- Has /etc/issue warning banner...",  "OK")
        mock_logger.info.assert_any_call("Has /etc/issue.net set, checking ok")
        mock_display.assert_any_call("- Has /etc/issue.net warning banner...",  "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.InsertSection')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.logger')
    @patch('secScanner.enhance.euler.check.C0228_warnBanner.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_files_no_exist(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟所有文件都不存在
        mock_exists.side_effect = lambda x: False
        secScanner.enhance.euler.check.C0228_warnBanner.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0228_warnBanner()

        mock_InsertSection.assert_any_call("check system warning  banner")
        mock_logger.warning.assert_any_call("WRN_C0228_01: %s", WRN_C0228_01)
        mock_logger.warning.assert_any_call("SUG_C0228_01: %s", SUG_C0228_01)
        mock_display.assert_any_call("- No /etc/motd set...", "WARNING")

        mock_logger.warning.assert_any_call("WRN_C0228_02: %s", WRN_C0228_02)
        mock_logger.warning.assert_any_call("SUG_C0228_02: %s", SUG_C0228_02)
        mock_display.assert_any_call("- No /etc/issue set...", "WARNING")

        mock_logger.warning.assert_any_call("WRN_C0228_03: %s", WRN_C0228_03)
        mock_logger.warning.assert_any_call("SUG_C0228_03: %s", SUG_C0228_03)
        mock_display.assert_any_call("- No /etc/issue.net set...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()