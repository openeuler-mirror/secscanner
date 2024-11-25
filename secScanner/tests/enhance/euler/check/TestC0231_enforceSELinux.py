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
from secScanner.enhance.euler.check.C0231_enforceSELinux import C0231_enforceSELinux
import secScanner

class TestC0231_enforceSELinux(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_exists(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        config_file = "/etc/selinux/config"
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0231_enforceSELinux.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0231_enforceSELinux()
        mock_InsertSection.assert_called_with("check the selinux set")
        mock_logger.warning.assert_any_call(f"WRN_C0231: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0231: {config_file} {SUG_no_file}")
        mock_display.assert_any_call(f"- Config file: {config_file} not found...", "SKIPPING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.Display')
    @patch('builtins.open', new_callable=mock_open, read_data="SELINUX=disabled")
    def test_selinux_disabled(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0231_enforceSELinux.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0231_enforceSELinux()
        mock_InsertSection.assert_called_with("check the selinux set")
        mock_logger.warning.assert_any_call("WRN_C0231: %s", WRN_C0231)
        mock_logger.warning.assert_any_call("SUG_C0231: %s", SUG_C0231)
        mock_display.assert_any_call("- Wrong selinux set...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.Display')
    @patch('builtins.open', new_callable=mock_open, read_data="SELINUX=enforcing")
    def test_selinux_enforcing(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = True
        # 调用测试函数
        C0231_enforceSELinux()
        mock_InsertSection.assert_called_with("check the selinux set")
        mock_logger.info.assert_any_call("Has right selinux set, checking ok")
        mock_display.assert_any_call("- Has right selinux set ...", "OK")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0231_enforceSELinux.Display')
    @patch('builtins.open', new_callable=mock_open, read_data="SELINUX=permissive")
    def test_selinux_permissive(self, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_exists.return_value = True
        # 调用测试函数
        C0231_enforceSELinux()
        mock_InsertSection.assert_called_with("check the selinux set")
        mock_logger.info.assert_any_call("Has right selinux set, checking ok")
        mock_display.assert_any_call("- Has right selinux set ...", "OK")

if __name__ == '__main__':
    unittest.main()