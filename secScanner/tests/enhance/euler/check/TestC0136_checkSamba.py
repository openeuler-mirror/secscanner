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
from secScanner.enhance.euler.check.C0136_checkSamba import C0136_checkSamba

class TestC0136_checkSamba(unittest.TestCase):
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(1,'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_installed(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        
        # 设置模拟返回值
        mock_exists.return_value = True
        mock_getsize.return_value = 10  # 假设文件非空
        
        # 调用测试函数
        C0136_checkSamba()
        
        mock_InsertSection.assert_called_once_with("Check whether the Samba software is installed in your Linux System ")
        mock_logger.info.assert_called_once_with('The samba status is: uninstalled')
        mock_display.assert_called_with("- Check the samba software is uninstall...", "OK")
        mock_file.assert_not_called()  # 确保没有写入文件
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(0,'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_uninstalled(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
       
        # 假设的全局变量
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 设置模拟返回值
        mock_exists.return_value = False
        mock_getsize.return_value = 0  # 文件为空
        
        # 调用测试函数
        C0136_checkSamba()
        mock_InsertSection.assert_called_once_with("Check whether the Samba software is installed in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0136: %s", WRN_C0136)
        mock_logger.warning.assert_any_call("SUG_C0136: %s", SUG_C0136)
        mock_display.assert_called_with('- Check the samba software is installed...', 'WARNING')        
        mock_file.assert_any_call("result_file_path", "a+")  # 检查是否尝试写入文件

    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_001_ret1_insert_section_once(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_002_ret1_file_not_opened(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        mock_file.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_003_ret1_logger_warning_not_called(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        mock_logger.warning.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_004_ret1_display_ok_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        args, _ = mock_display.call_args
        self.assertEqual(args[0], "- Check the samba software is uninstall...")
        self.assertEqual(args[1], "OK")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(2, 'not found'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_005_ret2_ok(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        mock_display.assert_called_once_with("- Check the samba software is uninstall...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(255, 'error'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_006_ret255_ok(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        mock_display.assert_called_once_with("- Check the samba software is uninstall...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_007_ret1_no_exception(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        try:
            C0136_checkSamba()
        except Exception as e:
            self.fail(f"C0136_checkSamba() raised an exception: {e}")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_008_ret1_logger_info_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        C0136_checkSamba()
        mock_logger.info.assert_called_once_with("The samba status is: uninstalled")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_009_ret0_insert_section_once(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"
        C0136_checkSamba()
        self.assertEqual(mock_InsertSection.call_count, 1)
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_010_ret0_logger_info_not_called(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"
        C0136_checkSamba()
        mock_logger.info.assert_not_called()
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_011_ret0_display_warning_exact(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"
        C0136_checkSamba()
        args, _ = mock_display.call_args
        self.assertEqual(args[0], "- Check the samba software is installed...")
        self.assertEqual(args[1], "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_012_ret0_logger_warning_twice(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"
        C0136_checkSamba()
        self.assertEqual(mock_logger.warning.call_count, 2)
    
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'installed'))
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.logger')
    @patch('secScanner.enhance.euler.check.C0136_checkSamba.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_013_ret0_file_open_aplus(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        secScanner.enhance.euler.check.C0136_checkSamba.RESULT_FILE = "result_file_path"
        C0136_checkSamba()
        mock_file.assert_called_with("result_file_path", "a+")

if __name__ == '__main':
    unittest.main()   