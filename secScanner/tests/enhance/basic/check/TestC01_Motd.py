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
import os
import sys
import secScanner
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C01_motd import C01_motd

class TestC01_Motd(unittest.TestCase):
    @patch('secScanner.enhance.basic.check.C01_motd.os.path.exists')
    @patch('secScanner.enhance.basic.check.C01_motd.os.path.getsize')
    @patch('secScanner.enhance.basic.check.C01_motd.logger')
    @patch('secScanner.enhance.basic.check.C01_motd.Display')
    @patch('secScanner.enhance.basic.check.C01_motd.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_motd_exists_and_not_empty(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_getsize, mock_exists):
        # 设置模拟返回值
        mock_exists.return_value = True
        mock_getsize.return_value = 10  # 假设文件非空

        # 调用测试函数
        C01_motd()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("check /etc/motd banner")
        mock_Display.assert_called_once_with("- Has /etc/motd set...", "OK")
        mock_logger.info.assert_called_once_with("Has /etc/motd set, checking ok")
        mock_file.assert_not_called()  # 确保没有写入文件
    
    @patch('secScanner.enhance.basic.check.C01_motd.os.path.exists')
    @patch('secScanner.enhance.basic.check.C01_motd.os.path.getsize')
    @patch('secScanner.enhance.basic.check.C01_motd.logger')
    @patch('secScanner.enhance.basic.check.C01_motd.Display')
    @patch('secScanner.enhance.basic.check.C01_motd.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_motd_not_exists_or_empty(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_getsize, mock_exists):
        # 设置模拟返回值
        mock_exists.return_value = False
        mock_getsize.return_value = 0  # 文件为空

        # 假设的全局变量
        secScanner.enhance.basic.check.C01_motd.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        #secScanner.enhance.basic.check.C01_motd.WRN_C01 = WRN_C01
        #secScanner.enhance.basic.check.SUG_C01 = SUG_C01

        # 调用测试函数
        C01_motd()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("check /etc/motd banner")
        mock_Display.assert_called_once_with("- No /etc/motd set...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C01: %s", WRN_C01)
        #mock_logger.warning.assert_any_call("SUG_C01: %s", SUG_C01)
        mock_file.assert_called_once_with("result_file_path", "a")  # 检查是否尝试写入文件

if __name__ == '__main__':
    unittest.main()

