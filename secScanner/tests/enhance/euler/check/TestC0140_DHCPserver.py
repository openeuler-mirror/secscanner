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
from secScanner.enhance.euler.check.C0140_DHCPserver import C0140_DHCPserver

class TestC0140_DHCPserver(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.logger')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_dhcp_not_installed(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟 dhcp 未安装的情况
        mock_getstatusoutput.side_effect = [(1, 'package dhcp is not installed')]
        
        # 调用测试函数
        C0140_DHCPserver()
        
        mock_InsertSection.assert_called_once_with("Check whether the status of DHCP Server in your Linux System ")
        mock_logger.info.assert_called_with("package dhcp is not installed")
        mock_display.assert_called_with("- package dhcp is not installed", "OK")

    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.logger')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_dhcp_installed_disabled(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟 dhcp 安装，且 dhcp 服务未启用的情况
        mock_getstatusoutput.side_effect = [(0, 'package dhcp is installed'), (1, 'disabled')]
        
        # 调用测试函数
        C0140_DHCPserver()
        mock_InsertSection.assert_called_once_with("Check whether the status of DHCP Server in your Linux System ")
        mock_logger.info.assert_called_with("The DHCP-Server status is: disabled")
        mock_display.assert_called_with("- Check the DHCP-Server is disabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.logger')
    @patch('secScanner.enhance.euler.check.C0140_DHCPserver.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_dhcp_installed_enabled(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟 dhcp 安装，且 dhcp 服务启用的情况
        mock_getstatusoutput.side_effect = [(0, 'package dhcp is installed'), (0, 'enabled')]
        # 假设的全局变量
        secScanner.enhance.euler.check.C0140_DHCPserver.RESULT_FILE = "result_file_path"  # 假设的结果文件路径

        # 调用测试函数
        C0140_DHCPserver()
        mock_InsertSection.assert_called_once_with("Check whether the status of DHCP Server in your Linux System ")
        mock_logger.warning.assert_any_call("WRN_C0140: %s", WRN_C0140)
        mock_logger.warning.assert_any_call("SUG_C0140: %s", SUG_C0140)
        mock_display.assert_called_with("- Check the DHCP-Server is enabled...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a+")  # 检查是否尝试写入文件

if __name__ == '__main__':
    unittest.main()