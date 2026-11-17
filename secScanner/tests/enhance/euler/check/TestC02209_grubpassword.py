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
import os
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02209_grubpassword import C02209_grubpassword  # Mock test setup.

GRUB_CFG = os.path.join('/boot/grub2', 'grub.cfg')
USER_CFG = os.path.join('/boot/grub2', 'user.cfg')

class TestC02209_grubpassword(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='menuentry openEuler {\n    linux /vmlinuz\n}\n')
    def test_no_password_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_isdir, mock_exists):
        # Mock test setup.
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C02209_grubpassword.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that grub is protected with a password")
        mock_file.assert_any_call(GRUB_CFG, 'r')
        mock_file.assert_any_call(USER_CFG, 'r')
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_with("\nC02209\n")
        mock_logger.warning.assert_any_call("WRN_C02209_01: %s", WRN_C02209_01)
        mock_logger.warning.assert_any_call("SUG_C02209_01: %s", SUG_C02209_01)
        mock_logger.warning.assert_any_call("WRN_C02209_02: %s", WRN_C02209_02)
        mock_logger.warning.assert_any_call("SUG_C02209_02: %s", SUG_C02209_02)
        mock_Display.assert_any_call("- No password_pbkdf2 set in grub.cfg...", "WARNING")
        mock_Display.assert_any_call("- No GRUB2_PASSWORD set in user.cfg...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data='password_pbkdf2 root grub.pbkdf2.sha512.10000.ABCDEF\n'
                     'GRUB2_PASSWORD=grub.pbkdf2.sha512.10000.ABCDEF\n')
    def test_password_set_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_isdir, mock_exists):
        # Mock test setup.
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        mock_exists.return_value = True

        # Mock test setup.
        C02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that grub is protected with a password")
        mock_logger.info.assert_called_once_with("grub password protection is set, checking ok")
        mock_Display.assert_called_once_with("- Has grub password protection set...", "OK")
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data='password_pbkdf2 root grub.pbkdf2.sha512.10000.ABCDEF\n')
    def test_user_cfg_missing_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_isdir, mock_exists):
        """边界：user.cfg 不存在，仅应告警 GRUB2_PASSWORD 一项并写入一次 RESULT_FILE"""
        # Mock test setup.
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        mock_exists.side_effect = lambda path: path.endswith('grub.cfg')

        # Mock test setup.
        secScanner.enhance.euler.check.C02209_grubpassword.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that grub is protected with a password")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_with("\nC02209\n")
        mock_logger.warning.assert_any_call("WRN_C02209_02: %s", WRN_C02209_02)
        mock_logger.warning.assert_any_call("SUG_C02209_02: %s", SUG_C02209_02)
        mock_Display.assert_called_once_with("- No GRUB2_PASSWORD set in user.cfg...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.check.C02209_grubpassword.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_grub_dir_missing_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_isdir, mock_exists):
        """边界：grub 配置目录均不存在，应 SKIPPING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_isdir.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C02209_grubpassword.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that grub is protected with a password")
        mock_exists.assert_not_called()
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC02209\n")
        mock_logger.warning.assert_any_call("WRN_C02209: /boot/efi/EFI/openEuler or /boot/grub2 %s", WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02209: /boot/efi/EFI/openEuler or /boot/grub2 %s", SUG_no_file)
        mock_Display.assert_called_once_with("- Grub config directory not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
