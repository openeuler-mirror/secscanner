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
from secScanner.enhance.euler.check.C0119_LdLibraryPath import C0119_LdLibraryPath

class TestC0119_LdLibraryPath(unittest.TestCase):
    
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.InsertSection')
    @patch('subprocess.getstatusoutput', return_value = (0, '/home/'))
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.logger')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='export LD_LIBRARY_PATH=/home/')
    def test_LdLibraryPat_value_set(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        
        # 设置模拟返回值
        mock_exists.side_effect = [True, True, True]  # 所有文件存在
        
        # 调用测试函数
        C0119_LdLibraryPath()
        mock_InsertSection.assert_called_once_with("Check the value of LD_LIBRARY_PATH in your Linux System ")
        mock_logger.info.assert_any_call("Check set of LD_LIBRARY_PATH in /etc/profile file")
        mock_display.assert_any_call("- The value of LD_LIBRARY_PATH is /home/ in /etc/profile file", "OK")        

    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.InsertSection')
    @patch('subprocess.getstatusoutput', return_value = (1, ''))
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.logger')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_LdLibraryPat_value_not_set(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        
        # 设置模拟返回值
        mock_exists.side_effect = [True, True, True]  # 所有文件存在
        
        # 调用测试函数
        C0119_LdLibraryPath()
        mock_InsertSection.assert_called_once_with("Check the value of LD_LIBRARY_PATH in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0119: %s", WRN_C0119)
        mock_logger.warning.assert_any_call("SUG_C0119: %s", SUG_C0119)
        mock_display.assert_any_call("- Wrong set of LD_LIBRARY_PATH in /etc/profile file...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.InsertSection')
    @patch('subprocess.getstatusoutput', return_value = (0, ''))
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.logger')
    @patch('secScanner.enhance.euler.check.C0119_LdLibraryPath.Display')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_file_not_exist(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        
        # 设置模拟返回值
        mock_exists.side_effect = [False, False, False]  # 所有文件不存在
        
        # 调用测试函数
        C0119_LdLibraryPath()
        mock_InsertSection.assert_called_once_with("Check the value of LD_LIBRARY_PATH in your Linux System ")
        mock_logger.warning.assert_any_call(f"WRN_C0119: /etc/profile {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0119: /etc/profile {SUG_no_file}")
        mock_display.assert_any_call("- Config file: /etc/profile not found...", "SKIPPING")      

if __name__ == '__main__':
    unittest.main()