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
import secScanner
from secScanner.enhance.level3.check.C132_disableTelnet import C132_disableTelnet  # 替换成实际的模块名
from secScanner.lib.textInfo_level3 import *
from secScanner.lib.textInfo_basic import *


class TestC132_disableTelnet(unittest.TestCase):
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.Display')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.logger')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.InsertSection')
    def test_telnet_disabled(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        # 调用函数
        C132_disableTelnet()

        mock_InsertSection.assert_called_once_with("Check if telnet is not enabled")
        # 检查 Display 函数是否被调用
        mock_display.assert_called_once_with("- Telnet not enabled...", "OK")
        # 检查日志记录
        mock_logger.info.assert_called_once_with("Telnet not enabled...")
        # 检查文件操作
        mock_file.assert_not_called()  # 确保没有写入文件

    @patch('subprocess.getstatusoutput', return_value=(0, ''))
    @patch('builtins.open', new_callable=mock_open)
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.Display')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.logger')
    @patch('secScanner.enhance.level3.check.C132_disableTelnet.InsertSection')
    def test_telnet_enabled(self, mock_InsertSection, mock_logger, mock_display, mock_file, mock_getstatusoutput):
        # 假设的全局变量
        secScanner.enhance.level3.check.C132_disableTelnet.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用函数
        C132_disableTelnet()

        mock_InsertSection.assert_called_once_with("Check if telnet is not enabled")
        # 检查 Display 函数是否被调用
        mock_display.assert_called_once_with("- Telnet enabled...", "WARNING")
        # 检查日志记录
        mock_logger.warning.assert_any_call("WRN_C132: %s", WRN_C132)
        mock_logger.warning.assert_any_call("SUG_C132: %s", SUG_C132)
        # 检查文件操作
        mock_file.assert_called_once_with("result_file_path", "a")  # 检查是否尝试写入文件

if __name__ == '__main__':
    unittest.main()