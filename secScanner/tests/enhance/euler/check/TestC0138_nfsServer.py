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
from secScanner.enhance.euler.check.C0138_nfsServer import C0138_nfsServer

class TestC0138_nfsServer(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0138_nfsServer.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0138_nfsServer.logger')
    @patch('secScanner.enhance.euler.check.C0138_nfsServer.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_nfs_not_installed(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟 nfs-utils 未安装的情况
        mock_getstatusoutput.side_effect = [(1, 'package nfs-utils is not installed')]
        
        # 调用测试函数
        C0138_nfsServer()
        
        mock_InsertSection.assert_called_once_with("Check whether the status of nfs-Server in your Linux System ")
        mock_logger.info.assert_called_with("package nfs-utils is not installed")
        mock_display.assert_called_with("- package nfs-utils is not installed", "OK")

    @patch('secScanner.enhance.euler.check.C0138_nfsServer.InsertSection')
    @patch('subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C0138_nfsServer.logger')
    @patch('secScanner.enhance.euler.check.C0138_nfsServer.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_nfs_installed_disabled(self, mock_open, mock_display, mock_logger, mock_getstatusoutput, mock_InsertSection):
        # 模拟 nfs-utils 安装，且nfs服务未启用的情况
        mock_getstatusoutput.side_effect = [(0, 'package nfs-utils is installed'), (1, 'disabled')]
        
        # 调用测试函数
        C0138_nfsServer()
        mock_InsertSection.assert_called_once_with("Check whether the status of nfs-Server in your Linux System ")
        mock_logger.info.assert_called_with("The nfs-Server status is: disabled")
        mock_display.assert_called_with("- Check the nfs-Server is disabled...", "OK")
    
if __name__ == '__main__':
    unittest.main()