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
from secScanner.enhance.euler.check.C03309_permitrootlogin import C03309_permitrootlogin  # Mock test setup.

CONFIG_FILE = "/etc/ssh/sshd_config"
SECTION = "Check set of PermitRootLogin in sshd config file"

class TestC03309_permitrootlogin(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin yes\n")
    def test_permit_root_login_yes_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03309_permitrootlogin.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03309\n")
        mock_logger.warning.assert_any_call("WRN_C03309: %s", WRN_C03309)
        mock_logger.warning.assert_any_call("SUG_C03309: %s", SUG_C03309)
        mock_Display.assert_called_once_with("- Wrong set of PermitRootLogin in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin no\n")
    def test_permit_root_login_no_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("- Check set of PermitRootLogin in sshd config file", "OK")

    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin yes # trailing comment\n")
    def test_permit_root_login_extra_field_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：PermitRootLogin 行带多余字段，len != 2 应判为不合规"""
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C03309_permitrootlogin.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03309\n")
        mock_Display.assert_called_once_with("- Wrong set of PermitRootLogin in sshd config file...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.check.C03309_permitrootlogin.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C03309_permitrootlogin.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_logger.warning.assert_any_call(f"WRN_C03309: {CONFIG_FILE} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C03309: {CONFIG_FILE} {SUG_no_file}")
        mock_Display.assert_called_once_with(f"- Config file: {CONFIG_FILE} not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
