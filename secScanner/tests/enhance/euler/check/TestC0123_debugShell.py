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
import secScanner
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0123_debugShell import C0123_debugShell 

class TestC0123_debugShell(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0123_debugShell.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(1,'disabled'))
    @patch('secScanner.enhance.euler.check.C0123_debugShell.logger')
    @patch('secScanner.enhance.euler.check.C0123_debugShell.Display')
    def test_debug_shell_server_disabled(self, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        
        # 调用测试函数
        C0123_debugShell()
        mock_InsertSection.assert_called_once_with("Check the debug-shell server's status in your Linux System ")
        mock_logger.info.assert_called_once_with("The status of debug-shell is disabled")
        mock_display.assert_called_once_with("- Check the status of debug-shell is disabled...", "OK")
        
    
    @patch('secScanner.enhance.euler.check.C0123_debugShell.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(0, 'enabled'))
    @patch('secScanner.enhance.euler.check.C0123_debugShell.logger')
    @patch('secScanner.enhance.euler.check.C0123_debugShell.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_debug_shell_server_enabled(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 假设的全局变量
        secScanner.enhance.euler.check.C0123_debugShell.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        
        # 调用测试函数
        C0123_debugShell()
        
        mock_InsertSection.assert_called_once_with("Check the debug-shell server's status in your Linux System ") 
        mock_display.assert_called_once_with("- Check the status of debug-shell is enabled...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0123: %s", WRN_C0123)
        mock_file.assert_called_once_with("result_file_path", "a+")  # 检查是否尝试写入文件

if __name__ == '__main':
    unittest.main()
