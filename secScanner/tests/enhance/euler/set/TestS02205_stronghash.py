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
from secScanner.enhance.euler.set.S02205_stronghash import S02205_stronghash


def _make_open(files, opened, writable=True):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        elif "a" in mode:
            files.setdefault(path, [])
            if writable:
                handle.write.side_effect = lambda data: files[path].append(data)
        elif "w" in mode:
            if writable:
                files[path] = []
                handle.writelines.side_effect = lambda lines: files.__setitem__(path, list(lines))
                handle.write.side_effect = lambda data: files[path].append(data)
        return handle
    return _open


def _make_exists(files):
    def _exists(path):
        if path.endswith("_bak"):
            return False
        return path in files
    return _exists


class TestS02205_stronghash(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02205_stronghash.seconf.get')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.InsertSection')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.Display')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.logger')
    def test_config_disabled_skipping(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02205_stronghash()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_stronghash')
        mock_InsertSection.assert_called_once_with("set that the password is encrypted with strong hash algorithm...")
        mock_Display.assert_called_once_with("- Skip set the password strong hash algorithm...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.seconf.get')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.InsertSection')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.Display')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.logger')
    def test_already_set_skipping(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get, mock_exists):
        """边界：三项配置均已满足时仅跳过"""
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so sha512 shadow nullok\n'],
            '/etc/login.defs': ['ENCRYPT_METHOD SHA512\n'],
            '/etc/libuser.conf': ['crypt_style = sha512\n'],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened)):
            S02205_stronghash()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_stronghash')
        mock_InsertSection.assert_called_once_with("set that the password is encrypted with strong hash algorithm...")
        mock_logger.info.assert_called_once_with("strong hash algorithm is already set")
        mock_Display.assert_called_once_with("- Already set the password strong hash algorithm...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02205_stronghash.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.seconf.get')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.InsertSection')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.Display')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.logger')
    def test_set_strong_hash_finished(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get,
                                      mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so md5 shadow nullok\n'],
            '/etc/login.defs': ['# login defs\n'],
            '/etc/libuser.conf': ['# libuser\n'],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened)):
            S02205_stronghash()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_stronghash')
        mock_InsertSection.assert_called_once_with("set that the password is encrypted with strong hash algorithm...")
        self.assertEqual(mock_copy2.call_count, 3)
        mock_add_bak_file.assert_any_call('/etc/pam.d/system-auth_bak')
        mock_add_bak_file.assert_any_call('/etc/login.defs_bak')
        mock_add_bak_file.assert_any_call('/etc/libuser.conf_bak')
        mock_logger.info.assert_called_once_with("set the password strong hash algorithm successfully")
        mock_Display.assert_called_once_with("- Set the password strong hash algorithm...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02205_stronghash.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.seconf.get')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.InsertSection')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.Display')
    @patch('secScanner.enhance.euler.set.S02205_stronghash.logger')
    def test_set_strong_hash_failed(self, mock_logger, mock_Display, mock_InsertSection, mock_seconf_get,
                                    mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        files = {
            '/etc/pam.d/system-auth': ['password    sufficient    pam_unix.so md5 shadow nullok\n'],
            '/etc/login.defs': ['# login defs\n'],
            '/etc/libuser.conf': ['# libuser\n'],
        }
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _make_exists(files)
        opened = []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, opened, writable=False)):
            S02205_stronghash()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set that the password is encrypted with strong hash algorithm...")
        mock_logger.warning.assert_called_once_with("set the password strong hash algorithm failed")
        mock_Display.assert_called_once_with("- Set the password strong hash algorithm...", "FAILED")

if __name__ == '__main__':
    unittest.main()
