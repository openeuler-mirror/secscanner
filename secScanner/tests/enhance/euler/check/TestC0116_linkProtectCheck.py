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
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_link_protection_case_01(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 01\n'

        C0116_linkProtectCheck()

        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")

        linkTypes = ["symlinks", "hardlinks"]
        for linkType in linkTypes:
            mock_logger.info.assert_any_call("Link type (%s) protection is enabled", linkType)
            mock_Display.assert_any_call("- Check whether %s fileprotection is enabled..." % linkType,"OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_link_protection_case_02(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 1 \n'

        C0116_linkProtectCheck()

        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")

        linkTypes = ["symlinks", "hardlinks"]
        for linkType in linkTypes:
            mock_logger.info.assert_any_call("Link type (%s) protection is enabled", linkType)
            mock_Display.assert_any_call("- Check whether %s fileprotection is enabled..." % linkType,"OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_003_symlinks_0_no_newline(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 末尾无换行符，值为 0"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 0'
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_004_symlinks_0_crlf(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 使用 Windows 换行 CRLF，值为 0"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 0\r\n'
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_005_symlinks_0_tab_separator(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """等号两侧使用制表符，值为 0"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks\t=\t0\n'
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_006_symlinks_1_trailing_spaces(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 末尾有多余空格，值为 1，应触发 OK"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 1   \n'
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_007_symlinks_1_leading_spaces(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 首部有多余空格，值为 1"""
        mock_subprocess.return_value.stdout = b'   fs.protected_symlinks = 1\n'
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_008_symlinks_1_no_newline(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 末尾无换行符，值为 1"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 1'
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_009_symlinks_1_crlf(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """stdout 使用 CRLF 换行，值为 1"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks = 1\r\n'
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_010_symlinks_1_tab_separator(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """等号两侧使用制表符，值为 1"""
        mock_subprocess.return_value.stdout = b'fs.protected_symlinks\t=\t1\n'
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_011_both_symlinks_0_hardlinks_0(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """symlinks=0 hardlinks=0 均 disabled"""
        mock_subprocess.return_value.stdout = (
            b'fs.protected_symlinks = 0\n'
            b'fs.protected_hardlinks = 0\n'
        )
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
        mock_Display.assert_any_call("- hardlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_012_both_symlinks_1_hardlinks_1(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """symlinks=1 hardlinks=1 均 enabled"""
        mock_subprocess.return_value.stdout = (
            b'fs.protected_symlinks = 1\n'
            b'fs.protected_hardlinks = 1\n'
        )
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
        mock_Display.assert_any_call("- Check whether hardlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_015_both_0_extra_blank_lines(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """输出中含空行，两者均为 0"""
        mock_subprocess.return_value.stdout = (
            b'\n'
            b'fs.protected_symlinks = 0\n'
            b'\n'
            b'fs.protected_hardlinks = 0\n'
        )
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
        mock_Display.assert_any_call("- hardlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_016_both_1_extra_blank_lines(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """输出中含空行，两者均为 1"""
        mock_subprocess.return_value.stdout = (
            b'\n'
            b'fs.protected_symlinks = 1\n'
            b'\n'
            b'fs.protected_hardlinks = 1\n'
        )
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
        mock_Display.assert_any_call("- Check whether hardlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_017_both_0_hardlinks_before_symlinks(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """hardlinks 行在 symlinks 行之前，两者均为 0"""
        mock_subprocess.return_value.stdout = (
            b'fs.protected_hardlinks = 0\n'
            b'fs.protected_symlinks = 0\n'
        )
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- symlinks protection is disabled...", "WARNING")
        mock_Display.assert_any_call("- hardlinks protection is disabled...", "WARNING")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    def test_018_both_1_hardlinks_before_symlinks(self, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """hardlinks 行在 symlinks 行之前，两者均为 1"""
        mock_subprocess.return_value.stdout = (
            b'fs.protected_hardlinks = 1\n'
            b'fs.protected_symlinks = 1\n'
        )
        C0116_linkProtectCheck()
        mock_Display.assert_any_call("- Check whether symlinks fileprotection is enabled...", "OK")
        mock_Display.assert_any_call("- Check whether hardlinks fileprotection is enabled...", "OK")
    
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.subprocess.run')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.InsertSection')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.Display')
    @patch('secScanner.enhance.euler.check.C0116_linkProtectCheck.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_019_both_0_uppercase_key(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_subprocess):
        """键名大写形式，值为 0"""
        mock_subprocess.return_value.stdout = (
            b'FS.PROTECTED_SYMLINKS = 0\n'
            b'FS.PROTECTED_HARDLINKS = 0\n'
        )
        secScanner.enhance.euler.check.C0116_linkProtectCheck.RESULT_FILE = "check_result.relt"
        C0116_linkProtectCheck()
        mock_InsertSection.assert_called_once_with("Check whether link file protection is enabled")
            
if __name__ == '__main__':
    unittest.main()