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
from secScanner.enhance.euler.check.C0134_Xwindows import C0134_Xwindows

class TestC0134_Xwindows(unittest.TestCase):
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(1,''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_installed(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        # 设置模拟返回值
        mock_exists.return_value = True
        mock_getsize.return_value = 10  # 假设文件非空
        
        # 调用测试函数
        C0134_Xwindows()
        
        mock_InsertSection.assert_called_once_with("Check whether the Xwindows software is installed in your Linux System ")
        mock_logger.info.assert_called_once_with('The xorg-x11 status is: ')
        mock_display.assert_called_with("- Check the xorg-x11 software is uninstall...", "OK")
        mock_file.assert_not_called()  # 确保没有写入文件
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(0,'installed'))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_uninstalled(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
       
        # 假设的全局变量
        secScanner.enhance.euler.check.C0134_Xwindows.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 设置模拟返回值
        mock_exists.return_value = False
        mock_getsize.return_value = 0  # 文件为空
        
        # 调用测试函数
        C0134_Xwindows()
        mock_InsertSection.assert_called_once_with("Check whether the Xwindows software is installed in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0134: %s", WRN_C0134)
        mock_logger.warning.assert_any_call("SUG_C0134: %s", SUG_C0134)
        mock_display.assert_called_with('- Check the xorg-x11 software is installed...', 'WARNING')        
        mock_file.assert_any_call("result_file_path", "a+")  # 检查是否尝试写入文件

    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_001_res_empty_insert_section_once(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_002_res_empty_file_not_opened(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        mock_file.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_003_res_empty_logger_warning_not_called(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        mock_logger.warning.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_004_res_empty_display_ok_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        args, _ = mock_display.call_args
        self.assertEqual(args[0], "- Check the xorg-x11 software is uninstall...")
        self.assertEqual(args[1], "OK")
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_005_ret0_res_empty_ok(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        mock_display.assert_called_once_with("- Check the xorg-x11 software is uninstall...", "OK")
        mock_file.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_006_res_empty_no_exception(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        try:
            C0134_Xwindows()
        except Exception as e:
            self.fail(f"C0134_Xwindows() raised an exception: {e}")
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, ''))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_007_res_empty_logger_info_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0134_Xwindows()
        mock_logger.info.assert_called_once_with("The xorg-x11 status is: ")
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'xorg-x11-server-Xorg'))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_008_res_nonempty_insert_section_once(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0134_Xwindows.RESULT_FILE = "result_file_path"
        C0134_Xwindows()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'xorg-x11-server-Xorg'))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_009_res_nonempty_logger_info_not_called(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0134_Xwindows.RESULT_FILE = "result_file_path"
        C0134_Xwindows()
        mock_logger.info.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'xorg-x11-server-Xorg'))
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.logger')
    @patch('secScanner.enhance.euler.check.C0134_Xwindows.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_010_res_nonempty_display_warning_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0134_Xwindows.RESULT_FILE = "result_file_path"
        C0134_Xwindows()
        args, _ = mock_display.call_args
        self.assertEqual(args[0], "- Check the xorg-x11 software is installed...")
        self.assertEqual(args[1], "WARNING")

if __name__ == '__main':
    unittest.main()    