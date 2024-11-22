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
from secScanner.enhance.euler.check.C0230_histsize import C0230_histsize
from secScanner.lib import *
import secScanner
class TestC0230_histsize(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="HISTSIZE=50")
    @patch('secScanner.enhance.euler.check.C0230_histsize.logger')
    @patch('secScanner.enhance.euler.check.C0230_histsize.Display')
    @patch('secScanner.enhance.euler.check.C0230_histsize.InsertSection')
    def test_C0230_histsize_correct(self, mock_InsertSection, mock_display, mock_logger, mock_open):
        # 调用测试函数
        C0230_histsize()
        mock_InsertSection.assert_any_call("check HISTSIZE of /etc/profile")
        mock_logger.info.assert_called_once_with("HISTSIZE set correctly, checking ok")
        mock_display.assert_called_once_with("- Has set HISTSIZE correctly ...", "OK")
    

    @patch('builtins.open', new_callable=mock_open, read_data="HISTSIZE=49")
    @patch('secScanner.enhance.euler.check.C0230_histsize.logger')
    @patch('secScanner.enhance.euler.check.C0230_histsize.Display')
    @patch('secScanner.enhance.euler.check.C0230_histsize.InsertSection')
    def test_C0230_histsize_too_small(self, mock_InsertSection, mock_display, mock_logger, mock_open):
        secScanner.enhance.euler.check.C0230_histsize.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0230_histsize()
        mock_InsertSection.assert_any_call("check HISTSIZE of /etc/profile")
        mock_logger.warning.assert_any_call("WRN_C0230: %s", WRN_C0230)
        mock_logger.warning.assert_any_call("SUG_C0230: %s", SUG_C0230)
        mock_display.assert_called_once_with("- Wrong HISTSIZE set...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
if __name__ == '__main__':
    unittest.main()