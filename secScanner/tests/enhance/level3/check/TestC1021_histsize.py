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
from secScanner.enhance.level3.check.C1021_histsize import C1021_histsize  # 替换为实际的模块路径

class TestC1021_histsize(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="HISTSIZE=60\n")
    @patch('secScanner.enhance.level3.check.C1021_histsize.InsertSection')
    @patch('secScanner.enhance.level3.check.C1021_histsize.os.path.exists')
    @patch('secScanner.enhance.level3.check.C1021_histsize.Display')
    @patch('secScanner.enhance.level3.check.C1021_histsize.logger')
    def test_hist_size_correct(self, mock_logger, mock_display, mock_exists, mock_insert, mock_file):
        # 模拟 /etc/passwd 存在
        mock_exists.return_value = True

        # 调用被测试函数
        C1021_histsize()

        # 验证函数行为
        mock_logger.info.assert_called_with("HISTSIZE set correctly, checking ok")
        mock_display.assert_called_with("- Has set HISTSIZE correctly ...", "OK")

    @patch('builtins.open', new_callable=mock_open, read_data="HISTSIZE=30\n")
    @patch('secScanner.enhance.level3.check.C1021_histsize.InsertSection')
    @patch('secScanner.enhance.level3.check.C1021_histsize.os.path.exists')
    @patch('secScanner.enhance.level3.check.C1021_histsize.Display')
    @patch('secScanner.enhance.level3.check.C1021_histsize.logger')
    def test_hist_size_incorrect(self, mock_logger, mock_display, mock_exists, mock_insert, mock_file):
        # 模拟 /etc/passwd 存在
        mock_exists.return_value = True

        # 调用被测试函数
        C1021_histsize()

        # 验证函数行为
        mock_logger.warning.assert_any_call("WRN_C1021: %s", WRN_C1021)
        mock_logger.warning.assert_any_call("SUG_C1021: %s", SUG_C1021)
        mock_display.assert_called_with("- Wrong HISTSIZE set...", "WARNING")

if __name__ == "__main__":
    unittest.main()
