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
from secScanner.enhance.euler.check.C02210_singlemodepassword import C02210_singlemodepassword  # Mock test setup.

RESCUE_SERVICE = '/usr/lib/systemd/system/rescue.service'
EMERGENCY_SERVICE = '/usr/lib/systemd/system/emergency.service'

class TestC02210_singlemodepassword(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='[Unit]\nExecStart=/bin/bash\n')
    def test_no_sulogin_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C02210_singlemodepassword.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02210_singlemodepassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that single user mode is protected with a password")
        mock_file.assert_any_call(RESCUE_SERVICE, 'r')
        mock_file.assert_any_call(EMERGENCY_SERVICE, 'r')
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_with("\nC02210\n")
        mock_logger.warning.assert_any_call("WRN_C02210_01: %s", WRN_C02210_01)
        mock_logger.warning.assert_any_call("SUG_C02210_01: %s", SUG_C02210_01)
        mock_logger.warning.assert_any_call("WRN_C02210_02: %s", WRN_C02210_02)
        mock_logger.warning.assert_any_call("SUG_C02210_02: %s", SUG_C02210_02)
        mock_Display.assert_any_call("- No systemd-sulogin-shell set in %s..." % RESCUE_SERVICE, "WARNING")
        mock_Display.assert_any_call("- No systemd-sulogin-shell set in %s..." % EMERGENCY_SERVICE, "WARNING")

    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data='[Unit]\nExecStart=-/usr/lib/systemd/systemd-sulogin-shell rescue\n')
    def test_sulogin_set_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True

        # Mock test setup.
        C02210_singlemodepassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that single user mode is protected with a password")
        mock_logger.info.assert_any_call("single user mode password protection is set in %s, checking ok" % RESCUE_SERVICE)
        mock_Display.assert_any_call("- Has systemd-sulogin-shell set in %s..." % RESCUE_SERVICE, "OK")
        mock_Display.assert_any_call("- Has systemd-sulogin-shell set in %s..." % EMERGENCY_SERVICE, "OK")
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.InsertSection')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.Display')
    @patch('secScanner.enhance.euler.check.C02210_singlemodepassword.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data='[Unit]\nExecStart=-/usr/lib/systemd/systemd-sulogin-shell emergency\n')
    def test_rescue_service_missing(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：rescue.service 不存在时应 SKIPPING，emergency.service 合规仍应 OK"""
        # Mock test setup.
        mock_exists.side_effect = lambda path: path == EMERGENCY_SERVICE

        # Mock test setup.
        secScanner.enhance.euler.check.C02210_singlemodepassword.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02210_singlemodepassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that single user mode is protected with a password")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_logger.warning.assert_any_call("WRN_C02210_01: %s %s" % (RESCUE_SERVICE, WRN_no_file))
        mock_logger.warning.assert_any_call("SUG_C02210_01: %s %s" % (RESCUE_SERVICE, SUG_no_file))
        mock_Display.assert_any_call("- Config file: %s not found..." % RESCUE_SERVICE, "SKIPPING")
        mock_Display.assert_any_call("- Has systemd-sulogin-shell set in %s..." % EMERGENCY_SERVICE, "OK")

if __name__ == '__main__':
    unittest.main()
