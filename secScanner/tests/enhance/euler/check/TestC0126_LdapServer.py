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
from secScanner.enhance.euler.check.C0126_LdapServer import C0126_LdapServer

class TestC0126_LdapServer(unittest.TestCase):
    
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(1,'uninstalled'))
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.logger')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_installed(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
        # 设置模拟返回值
        mock_exists.return_value = True
        mock_getsize.return_value = 10  # 假设文件非空
        
        # 调用测试函数
        C0126_LdapServer()
        
        mock_InsertSection.assert_called_once_with("Check whether the LdapServer software is installed in your Linux System ")
        mock_logger.info.assert_called_once_with('The openldap-servers status is: uninstalled')
        mock_display.assert_called_with("- Check the openldap-servers software is uninstall...", "OK")
        mock_file.assert_not_called()  # 确保没有写入文件
    
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.os.path.getsize')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.InsertSection')
    @patch('subprocess.getstatusoutput',return_value=(0,'installed'))
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.logger')
    @patch('secScanner.enhance.euler.check.C0126_LdapServer.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_LdapServer_uninstalled(self, mock_file, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection, mock_getsize, mock_exists):
       
        # 假设的全局变量
        secScanner.enhance.euler.check.C0126_LdapServer.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 设置模拟返回值
        mock_exists.return_value = False
        mock_getsize.return_value = 0  # 文件为空
        
        # 调用测试函数
        C0126_LdapServer()
        mock_InsertSection.assert_called_once_with("Check whether the LdapServer software is installed in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0126: %s", WRN_C0126)
        mock_logger.warning.assert_any_call("SUG_C0126: %s", SUG_C0126)
        mock_display.assert_called_with("- Check the openldap-servers software is installed...", "WARNING")        
        mock_file.assert_any_call("result_file_path", "a+")  # 检查是否尝试写入文件

if __name__ == '__main':
    unittest.main()    