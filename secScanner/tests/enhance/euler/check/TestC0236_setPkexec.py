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
from secScanner.enhance.euler.check.C0236_setPkexec import C0236_setPkexec
import secScanner

content_to_write = """
polkit.addAdminRule(function(action, subject) {
    return ["unix-user:0"];
});
"""

content_no_write = """
polkit.addAdminRule(function(action, subject) {
    return ["unix-user:1"];
});
"""
class TestC0236_setPkexec(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.logger')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.Display')
    @patch('builtins.open', new_callable=mock_open, read_data=content_to_write)
    def test_file_exists_and_content(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟文件存在且包含指定内容
        mock_exists.return_value = True
        # 调用测试函数
        C0236_setPkexec()
        mock_InsertSection.assert_any_call("check ordinary users cannot use pkexec to configure root privileges set")
        mock_logger.info.assert_any_call("check ordinary users cannot use pkexec to configure root privileges, checking ok")
        mock_display.assert_any_call("- check ordinary users cannot use pkexec to configure root privileges set...", "OK")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.InsertSection')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.logger')
    @patch('secScanner.enhance.euler.check.C0236_setPkexec.Display')
    @patch('builtins.open', new_callable=mock_open, read_data=content_no_write)
    def test_file_exists_but_content_missing(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        # 模拟文件存在但不包含指定内容
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0236_setPkexec.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0236_setPkexec()
        mock_InsertSection.assert_any_call("check ordinary users cannot use pkexec to configure root privileges set")
        mock_logger.warning.assert_any_call("WRN_C0236_01: %s", WRN_C0236_01)
        mock_logger.warning.assert_any_call("SUG_C0236_01: %s", SUG_C0236_01)
        mock_display.assert_any_call("- NO ordinary users cannot use pkexec to configure root privileges set...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()