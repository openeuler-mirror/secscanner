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
from secScanner.enhance.euler.check.C03303_sshkex import C03303_sshkex


class TestC03303_sshkex(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.Display')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256\n")
    def test_safe_kex_config_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of KexAlgorithms in sshd config file")
        mock_file.assert_called_once_with("/etc/ssh/sshd_config", "r")
        mock_logger.info.assert_called_once_with("Check set of KexAlgorithms in sshd config file")
        mock_Display.assert_called_once_with("- Check set of KexAlgorithms in sshd config file", "OK")

    @patch('secScanner.enhance.euler.check.C03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.Display')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="KexAlgorithms diffie-hellman-group14-sha1\n")
    def test_unsafe_kex_config_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03303_sshkex.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of KexAlgorithms in sshd config file")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03303\n")
        mock_logger.warning.assert_any_call("WRN_C03303: %s", WRN_C03303)
        mock_logger.warning.assert_any_call("SUG_C03303: %s", SUG_C03303)
        mock_Display.assert_called_once_with("- Wrong set of KexAlgorithms in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.Display')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="KexAlgorithms curve25519-sha256,diffie-hellman-group14-sha1\n")
    def test_mixed_kex_config_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：算法列表同时包含安全与不安全算法，应视为不合规"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03303_sshkex.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03303_sshkex()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03303\n")
        mock_logger.warning.assert_any_call("WRN_C03303: %s", WRN_C03303)
        mock_Display.assert_called_once_with("- Wrong set of KexAlgorithms in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03303_sshkex.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.InsertSection')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.Display')
    @patch('secScanner.enhance.euler.check.C03303_sshkex.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_exist_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：配置文件不存在时应 SKIPPING 并写入结果文件"""
        # Mock test setup.
        mock_exists.return_value = False
        config_file = "/etc/ssh/sshd_config"

        # Mock test setup.
        secScanner.enhance.euler.check.C03303_sshkex.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03303_sshkex()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check set of KexAlgorithms in sshd config file")
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03303\n")
        mock_logger.warning.assert_any_call(f"WRN_C03303: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C03303: {config_file} {SUG_no_file}")
        mock_Display.assert_called_once_with(f"- Config file: {config_file} not found...", "SKIPPING")


if __name__ == '__main__':
    unittest.main()
