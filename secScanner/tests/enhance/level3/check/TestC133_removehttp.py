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
from unittest.mock import patch, call, mock_open
import secScanner
from secScanner.enhance.level3.check.C133_removehttp import C133_removehttp  # 替换成实际的模块名
from secScanner.lib.textInfo_level3 import *
from secScanner.lib.textInfo_basic import *

# 设置测试环境
class TestC133_removehttp(unittest.TestCase):
    @patch('subprocess.getstatusoutput', return_value=(0, "httpd-2.4.6-93.el7.centos.x86_64"))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C133_removehttp.Display')
    @patch('secScanner.enhance.level3.check.C133_removehttp.logger')
    @patch('secScanner.enhance.level3.check.C133_removehttp.InsertSection')
    def test_http_installed(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        # 假设的全局变量
        secScanner.enhance.level3.check.C133_removehttp.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        C133_removehttp()
        mock_InsertSection.assert_called_once_with("Check if software HTTP exists")
        mock_logger.warning.assert_any_call("WRN_C133_01: %s", WRN_C133_01)
        mock_logger.warning.assert_any_call("SUG_C133_01: %s", SUG_C133_01)
        # 检查 Display 函数是否被调用
        mock_display.assert_called_once_with("- HTTP not removed...", "WARNING")
        # 检查文件操作
        mock_file.assert_called_once_with("result_file_path", "a")  # 检查是否尝试写入文件

    @patch('subprocess.getstatusoutput', return_value=(0, ""))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C133_removehttp.Display')
    @patch('secScanner.enhance.level3.check.C133_removehttp.logger')
    @patch('secScanner.enhance.level3.check.C133_removehttp.InsertSection')
    def test_http_not_installed(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        C133_removehttp()
        # 检查 Display 函数是否被调用
        mock_display.assert_called_once_with("- check http not installed...", "OK")
        # 检查日志记录
        mock_logger.info.assert_called_once_with("Http not installed, checking ok...")

if __name__ == '__main__':
    unittest.main()
