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
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03308_sshcryptooverride import C03308_sshcryptooverride  # Mock test setup.

CONFIG_FILE = "/etc/sysconfig/sshd"
SECTION = "Check crypto policy override of sshd"

class TestC03308_sshcryptooverride(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="CRYPTO_POLICY=DEFAULT\n")
    def test_crypto_policy_found_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03308_sshcryptooverride.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03308\n")
        mock_logger.warning.assert_any_call("WRN_C03308: %s", WRN_C03308)
        mock_logger.warning.assert_any_call("SUG_C03308: %s", SUG_C03308)
        mock_Display.assert_called_once_with("- Found crypto policy override of sshd...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="# CRYPTO_POLICY=DEFAULT\n")
    def test_no_crypto_policy_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("- Check crypto policy override of sshd", "OK")

    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="CRYPTO_POLICY=\n")
    def test_empty_crypto_policy_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：CRYPTO_POLICY 为空值，应视为未覆盖加密策略"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file().write.assert_not_called()
        mock_Display.assert_called_once_with("- Check crypto policy override of sshd", "OK")

    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.check.C03308_sshcryptooverride.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = False

        # Mock test setup.
        C03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("file /etc/sysconfig/sshd does not exist, no crypto policy override")
        mock_Display.assert_called_once_with("- Check crypto policy override of sshd", "OK")

if __name__ == '__main__':
    unittest.main()
