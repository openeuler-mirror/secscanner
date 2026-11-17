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
from unittest.mock import patch, MagicMock
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02204_pwordaccount import C02204_pwordaccount

RESULT = "check_result.relt"
SYSTEM_AUTH = '/etc/pam.d/system-auth'
PASSWORD_AUTH = '/etc/pam.d/password-auth'


def _make_open(files, written, opened):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        else:
            handle.write.side_effect = lambda data: written.append((path, data))
        return handle
    return _open


def _make_exists(files):
    return lambda path: path in files


class TestC02204_pwordaccount(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.InsertSection')
    def test_pam_pwquality_not_configured_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            SYSTEM_AUTH: ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            PASSWORD_AUTH: ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02204_pwordaccount.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02204_pwordaccount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the password does not contain the account string")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02204\n"), (RESULT, "\nC02204\n")])
        mock_logger.warning.assert_any_call("WRN_C02204_01: %s", WRN_C02204_01)
        mock_logger.warning.assert_any_call("SUG_C02204_01: %s", SUG_C02204_01)
        mock_logger.warning.assert_any_call("WRN_C02204_03: %s", WRN_C02204_03)
        mock_logger.warning.assert_any_call("SUG_C02204_03: %s", SUG_C02204_03)
        mock_Display.assert_any_call("- No pam_pwquality set in /etc/pam.d/system-auth...", "WARNING")
        mock_Display.assert_any_call("- No pam_pwquality set in /etc/pam.d/password-auth...", "WARNING")
        self.assertEqual(mock_Display.call_count, 2)

    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.InsertSection')
    def test_pam_pwquality_configured_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            SYSTEM_AUTH: ['password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root\n'],
            PASSWORD_AUTH: ['password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02204_pwordaccount()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the password does not contain the account string")
        self.assertEqual(written, [])
        mock_logger.info.assert_any_call(
            "pam_pwquality is enabled and no usercheck=0 set in /etc/pam.d/system-auth, checking ok")
        mock_logger.info.assert_any_call(
            "pam_pwquality is enabled and no usercheck=0 set in /etc/pam.d/password-auth, checking ok")
        mock_Display.assert_any_call(
            "- Has pam_pwquality set without usercheck=0 in /etc/pam.d/system-auth...", "OK")
        mock_Display.assert_any_call(
            "- Has pam_pwquality set without usercheck=0 in /etc/pam.d/password-auth...", "OK")
        self.assertEqual(mock_Display.call_count, 2)

    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.InsertSection')
    def test_usercheck_zero_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：system-auth 中 usercheck=0 应单独告警，password-auth 合规应判 OK"""
        # Mock test setup.
        files = {
            SYSTEM_AUTH: ['password    requisite     pam_pwquality.so minlen=8 usercheck=0\n'],
            PASSWORD_AUTH: ['password    requisite     pam_pwquality.so minlen=8\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02204_pwordaccount.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02204_pwordaccount()

        # Mock test setup.
        self.assertEqual(written, [(RESULT, "\nC02204\n")])
        mock_logger.warning.assert_any_call("WRN_C02204_02: %s", WRN_C02204_02)
        mock_logger.warning.assert_any_call("SUG_C02204_02: %s", SUG_C02204_02)
        mock_Display.assert_any_call("- usercheck=0 set in /etc/pam.d/system-auth...", "WARNING")
        mock_Display.assert_any_call(
            "- Has pam_pwquality set without usercheck=0 in /etc/pam.d/password-auth...", "OK")
        self.assertEqual(mock_Display.call_count, 2)

    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.check.C02204_pwordaccount.InsertSection')
    def test_both_config_missing_skipping(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：两个配置文件均不存在时应各写一次结果并跳过"""
        # Mock test setup.
        files = {}
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02204_pwordaccount.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02204_pwordaccount()

        # Mock test setup.
        self.assertEqual(written, [(RESULT, "\nC02204\n"), (RESULT, "\nC02204\n")])
        mock_logger.warning.assert_any_call("WRN_C02204_01: /etc/pam.d/system-auth " + WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02204_01: /etc/pam.d/system-auth " + SUG_no_file)
        mock_logger.warning.assert_any_call("WRN_C02204_03: /etc/pam.d/password-auth " + WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02204_03: /etc/pam.d/password-auth " + SUG_no_file)
        mock_Display.assert_any_call("- Config file: /etc/pam.d/system-auth not found...", "SKIPPING")
        mock_Display.assert_any_call("- Config file: /etc/pam.d/password-auth not found...", "SKIPPING")
        self.assertEqual(mock_Display.call_count, 2)

if __name__ == '__main__':
    unittest.main()
