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
from secScanner.enhance.euler.check.C02205_stronghash import C02205_stronghash

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


class TestC02205_stronghash(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.logger')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.Display')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.InsertSection')
    def test_sha512_not_configured_warning(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so md5 shadow nullok\n'],
            '/etc/login.defs': ['ENCRYPT_METHOD SHA512\n'],
            '/etc/libuser.conf': ['crypt_style = sha512\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02205_stronghash.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02205_stronghash()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the password is encrypted with strong hash algorithm")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02205\n")])
        mock_logger.warning.assert_any_call("WRN_C02205_01: %s", WRN_C02205_01)
        mock_logger.warning.assert_any_call("SUG_C02205_01: %s", SUG_C02205_01)
        mock_Display.assert_any_call("- No sha512 set for pam_unix in /etc/pam.d/system-auth...", "WARNING")
        mock_Display.assert_any_call("- Has ENCRYPT_METHOD SHA512 set in /etc/login.defs...", "OK")
        mock_Display.assert_any_call("- Has crypt_style sha512 set in /etc/libuser.conf...", "OK")

    @patch('secScanner.enhance.euler.check.C02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.logger')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.Display')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.InsertSection')
    def test_strong_hash_already_configured_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            '/etc/login.defs': ['ENCRYPT_METHOD SHA512\n'],
            '/etc/libuser.conf': ['crypt_style = sha512\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02205_stronghash()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the password is encrypted with strong hash algorithm")
        self.assertEqual(written, [])
        mock_logger.info.assert_any_call("strong hash algorithm is set in /etc/pam.d/system-auth, checking ok")
        mock_logger.info.assert_any_call("strong hash algorithm is set in /etc/login.defs, checking ok")
        mock_logger.info.assert_any_call("strong hash algorithm is set in /etc/libuser.conf, checking ok")
        mock_Display.assert_any_call("- Has sha512 set for pam_unix in /etc/pam.d/system-auth...", "OK")
        mock_Display.assert_any_call("- Has ENCRYPT_METHOD SHA512 set in /etc/login.defs...", "OK")
        mock_Display.assert_any_call("- Has crypt_style sha512 set in /etc/libuser.conf...", "OK")

    @patch('secScanner.enhance.euler.check.C02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.logger')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.Display')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.InsertSection')
    def test_libuser_conf_missing_skipping(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：libuser.conf 不存在时应写结果并跳过该项检查"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            '/etc/login.defs': ['ENCRYPT_METHOD SHA512\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []
        secScanner.enhance.euler.check.C02205_stronghash.RESULT_FILE = RESULT

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02205_stronghash()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("check that the password is encrypted with strong hash algorithm")
        self.assertIn((RESULT, "a", "utf-8"), opened)
        self.assertEqual(written, [(RESULT, "\nC02205\n")])
        mock_logger.warning.assert_any_call("WRN_C02205_03: /etc/libuser.conf " + WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02205_03: /etc/libuser.conf " + SUG_no_file)
        mock_Display.assert_any_call("- Config file: /etc/libuser.conf not found...", "SKIPPING")
        mock_Display.assert_any_call("- Has sha512 set for pam_unix in /etc/pam.d/system-auth...", "OK")

    @patch('secScanner.enhance.euler.check.C02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.logger')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.Display')
    @patch('secScanner.enhance.euler.check.C02205_stronghash.InsertSection')
    def test_crypt_style_uppercase_sha512_ok(self, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        """边界：crypt_style 的 sha512 大小写不敏感，应判定合规"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            '/etc/login.defs': ['ENCRYPT_METHOD SHA512\n'],
            '/etc/libuser.conf': ['# crypt style\n', 'crypt_style = SHA512\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            C02205_stronghash()

        # Mock test setup.
        self.assertEqual(written, [])
        mock_Display.assert_any_call("- Has crypt_style sha512 set in /etc/libuser.conf...", "OK")
        mock_Display.assert_any_call("- Has sha512 set for pam_unix in /etc/pam.d/system-auth...", "OK")

if __name__ == '__main__':
    unittest.main()
