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
import subprocess
import logging
import secScanner
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0116_linkProtectCheck import C0116_linkProtectCheck  # 替换为实际的模块路径

class TestC0116_linkProtectCheck(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_link_protection_disabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        # 设置模拟返回值
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 0\n'

        # 假设的全局变量
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"  # 假设的结果文件路径
        
        # 调用测试函数
        C0116_linkProtectCheck()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        linkTypes = ["symlinks", "hardlinks"]
        warnMessage = [WRN_C0116_01, WRN_C0116_02]
        sugMessage = [SUG_C0116_01, SUG_C0116_02]
        for i in range(len(linkTypes)):
            linkType = linkTypes[i]
            mock_file.assert_called_with("check_result.relt", "a")
            mock_logger.warning.assert_any_call("WRN_C0116_0%d: %s", (i + 1), warnMessage[i])
            mock_logger.warning.assert_any_call("SUG_C0116_0%d: %s", (i + 1), sugMessage[i])
            mock_Display.assert_any_call("- %s protection is disabled..." % linkType, "WARNING")
            

    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_link_protection_enabled(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        # 设置模拟返回值
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 1\n'
        
        # 调用测试函数
        C0116_linkProtectCheck()

        # 检查期望的调用和行为
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        linkTypes = ["symlinks", "hardlinks"]

        for i in range(len(linkTypes)):
            linkType = linkTypes[i]
            mock_logger.info.assert_any_call("Link type (%s) protection is enabled", linkType)
            mock_Display.assert_any_call("- Check whether %s fileprotection is enabled..." % linkType, "OK")
            
if __name__ == '__main__':
    unittest.main()