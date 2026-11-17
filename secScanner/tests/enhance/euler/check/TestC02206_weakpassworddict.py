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
from secScanner.enhance.euler.check.C02206_weakpassworddict import C02206_weakpassworddict

RESULT = "check_result.relt"


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


class TestC02206_weakpassworddict(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.logger')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.InsertSection')
    def test_pam_pwquality_not_enabled_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            '/etc/security/pwquality.conf': ['minlen = 8\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02206_weakpassworddict.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02206_weakpassworddict()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the weak password dictionary is set correctly")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02206\n")])
        mock_logger.warning.assert_any_call("WRN_C02206_01: %s", WRN_C02206_01)
        mock_logger.warning.assert_any_call("SUG_C02206_01: %s", SUG_C02206_01)
        mock_Display.assert_any_call("- No pam_pwquality set in /etc/pam.d/system-auth...", "WARNING")
        mock_Display.assert_any_call("- No dictcheck=0 set for pam_pwquality in /etc/pam.d/system-auth...", "OK")
        mock_Display.assert_any_call("- Has cracklib weak password dictionary in /usr/share/cracklib...", "OK")

    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.logger')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.InsertSection')
    def test_weak_password_dict_configured_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass local_users_only\n'],
            '/etc/security/pwquality.conf': ['# quality\n', 'minlen = 8\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02206_weakpassworddict()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the weak password dictionary is set correctly")
        self.assertEqual(written, [])
        mock_logger.info.assert_any_call("weak password dictionary check /etc/pam.d/system-auth is ok")
        mock_logger.info.assert_any_call("weak password dictionary check /etc/security/pwquality.conf is ok")
        mock_Display.assert_any_call("- Has pam_pwquality set in /etc/pam.d/system-auth...", "OK")
        mock_Display.assert_any_call("- No dictcheck=0 set for pam_pwquality in /etc/pam.d/system-auth...", "OK")
        mock_Display.assert_any_call("- No dictcheck=0 set in /etc/security/pwquality.conf...", "OK")
        mock_Display.assert_any_call("- Has cracklib weak password dictionary in /usr/share/cracklib...", "OK")

    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.logger')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.InsertSection')
    def test_cracklib_dict_missing_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：cracklib 弱口令字典不存在时应判定不合规"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass local_users_only\n'],
            '/etc/security/pwquality.conf': ['minlen = 8\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02206_weakpassworddict.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02206_weakpassworddict()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the weak password dictionary is set correctly")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02206\n")])
        mock_logger.warning.assert_any_call("WRN_C02206_04: %s", WRN_C02206_04)
        mock_logger.warning.assert_any_call("SUG_C02206_04: %s", SUG_C02206_04)
        mock_Display.assert_any_call("- No cracklib weak password dictionary in /usr/share/cracklib...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.logger')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.Display')
    @patch('secScanner.enhance.euler.check.C02206_weakpassworddict.InsertSection')
    def test_dictcheck_zero_in_both_files_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：system-auth 与 pwquality.conf 同时存在 dictcheck=0 时各记一次结果"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_pwquality.so try_first_pass dictcheck=0\n'],
            '/etc/security/pwquality.conf': ['dictcheck = 0\n'],
            '/usr/share/cracklib/pw_dict.hwm': [],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02206_weakpassworddict.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02206_weakpassworddict()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the weak password dictionary is set correctly")
        self.assertEqual(written, [(RESULT, "\nC02206\n"), (RESULT, "\nC02206\n")])
        mock_Display.assert_any_call("- dictcheck=0 set for pam_pwquality in /etc/pam.d/system-auth...", "WARNING")
        mock_Display.assert_any_call("- dictcheck=0 set in /etc/security/pwquality.conf...", "WARNING")
        mock_Display.assert_any_call("- Has pam_pwquality set in /etc/pam.d/system-auth...", "OK")

if __name__ == '__main__':
    unittest.main()
