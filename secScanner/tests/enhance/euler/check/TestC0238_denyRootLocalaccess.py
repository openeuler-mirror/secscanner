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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0238_denyRootLocalaccess import C0238_denyRootLocalaccess
import secScanner

class TestC0238_denyRootLocalaccess(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.InsertSection')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.logger')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_file_not_exist(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0238_denyRootLocalaccess.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0238_denyRootLocalaccess()
        mock_InsertSection.assert_any_call("check prevent root users from accessing the system locally")
        mock_logger.warning.assert_any_call("WRN_C0238_02: %s", WRN_C0238_02)
        mock_logger.warning.assert_any_call("SUG_C0238_02: %s", SUG_C0238_02)
        mock_display.assert_any_call("- file /etc/pam.d/system-auth does not exist...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.InsertSection')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.logger')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_pam_module_exists_but_tty1_not_denied(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0238_denyRootLocalaccess.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 模拟文件内容
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "auth required pam_access.so\n",
            "#-:root:tty1\n"
        ]
        # 调用测试函数
        C0238_denyRootLocalaccess()
        mock_InsertSection.assert_any_call("check prevent root users from accessing the system locally")
        mock_logger.warning.assert_any_call("WRN_C0238_01: %s", WRN_C0238_01)
        mock_logger.warning.assert_any_call("SUG_C0238_01: %s", SUG_C0238_01)
        mock_display.assert_any_call("- NO prevent root users from accessing the system locally set...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.InsertSection')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.logger')
    @patch('secScanner.enhance.euler.check.C0238_denyRootLocalaccess.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_pam_module_exists_and_tty1_exists(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0238_denyRootLocalaccess.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 模拟文件内容
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "auth required pam_access.so\n",
            "-:root:tty1\n"
        ]
        # 调用测试函数
        C0238_denyRootLocalaccess()
        mock_InsertSection.assert_any_call("check prevent root users from accessing the system locally")
        mock_logger.info.assert_any_call("check prevent root users from accessing the system locally, checking ok")
        mock_display.assert_any_call("- check prevent root users from accessing the system locally...", "OK")

if __name__ == '__main__':
    unittest.main()