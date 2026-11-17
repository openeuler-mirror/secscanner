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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03306_sshmacs import C03306_sshmacs


class TestC03306_sshmacs(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="MACs hmac-sha2-512,hmac-sha2-256,hmac-sha2-512-etm@openssh.com\n")
    def test_safe_macs_config_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of MACs in sshd config file")
        mock_file.assert_called_once_with("/etc/ssh/sshd_config", "r")
        mock_logger.info.assert_called_once_with("Check set of MACs in sshd config file")
        mock_Display.assert_called_once_with("- Check set of MACs in sshd config file", "OK")

    @patch('secScanner.enhance.euler.check.C03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="MACs hmac-md5,hmac-sha1\n")
    def test_unsafe_macs_config_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03306_sshmacs.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of MACs in sshd config file")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03306\n")
        mock_logger.warning.assert_any_call("WRN_C03306: %s", WRN_C03306)
        mock_logger.warning.assert_any_call("SUG_C03306: %s", SUG_C03306)
        mock_Display.assert_called_once_with("- Wrong set of MACs in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="macs hmac-sha2-512,hmac-md5\n")
    def test_mixed_macs_config_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：关键字小写且算法列表混入弱算法，应视为不合规"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03306_sshmacs.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03306_sshmacs()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03306\n")
        mock_logger.warning.assert_any_call("WRN_C03306: %s", WRN_C03306)
        mock_Display.assert_called_once_with("- Wrong set of MACs in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03306_sshmacs.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.InsertSection')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.Display')
    @patch('secScanner.enhance.euler.check.C03306_sshmacs.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_exist_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：配置文件不存在时应 SKIPPING 并写入结果文件"""
        # Mock test setup.
        mock_exists.return_value = False
        config_file = "/etc/ssh/sshd_config"

        # Mock test setup.
        secScanner.enhance.euler.check.C03306_sshmacs.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03306_sshmacs()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of MACs in sshd config file")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03306\n")
        mock_logger.warning.assert_any_call(f"WRN_C03306: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C03306: {config_file} {SUG_no_file}")
        mock_Display.assert_called_once_with(f"- Config file: {config_file} not found...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
