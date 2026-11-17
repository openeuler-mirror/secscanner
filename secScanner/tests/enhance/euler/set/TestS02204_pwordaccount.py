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
from secScanner.enhance.euler.set.S02204_pwordaccount import S02204_pwordaccount

SYSTEM_AUTH = '/etc/pam.d/system-auth'
PASSWORD_AUTH = '/etc/pam.d/password-auth'
PWQUALITY_LINE = ('password    requisite     pam_pwquality.so minlen=8 minclass=3 enforce_for_root '
                  'try_first_pass local_users_only retry=3 dcredit=0 ucredit=0 lcredit=0 ocredit=0\n')


def _make_open(files, written, opened, persist=True):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(files.get(path, []))
        else:
            def _writelines(lines):
                written.append((path, list(lines)))
                if persist:
                    files[path] = list(lines)
            handle.writelines.side_effect = _writelines
        return handle
    return _open


def _make_exists(files):
    return lambda path: path in files


class TestS02204_pwordaccount(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.InsertSection')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open({}, written, opened)):
            S02204_pwordaccount()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_pwordaccount')
        mock_InsertSection.assert_called_once_with("set that the password does not contain the account string...")
        mock_Display.assert_called_once_with(
            "- Skip set that the password does not contain the account string...", "SKIPPING")
        self.assertEqual(written, [])
        self.assertEqual(opened, [])
        mock_add_bak_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_exists.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.InsertSection')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.seconf.get')
    def test_set_pwquality_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                    mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        files = {
            SYSTEM_AUTH: ['password    requisite     pam_pwquality.so minlen=8 usercheck=0\n'],
            PASSWORD_AUTH: ['auth        required      pam_env.so\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            S02204_pwordaccount()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_pwordaccount')
        mock_InsertSection.assert_called_once_with("set that the password does not contain the account string...")
        mock_copy2.assert_any_call(SYSTEM_AUTH, SYSTEM_AUTH + '_bak')
        mock_copy2.assert_any_call(PASSWORD_AUTH, PASSWORD_AUTH + '_bak')
        mock_add_bak_file.assert_any_call(SYSTEM_AUTH + '_bak')
        mock_add_bak_file.assert_any_call(PASSWORD_AUTH + '_bak')
        self.assertEqual(written, [
            (SYSTEM_AUTH, ['password requisite pam_pwquality.so minlen=8\n']),
            (PASSWORD_AUTH, ['auth        required      pam_env.so\n', PWQUALITY_LINE]),
        ])
        mock_logger.info.assert_called_once_with("set that the password does not contain the account string successfully")
        mock_Display.assert_called_once_with(
            "- Set that the password does not contain the account string...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.InsertSection')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.seconf.get')
    def test_set_pwquality_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        files = {
            SYSTEM_AUTH: ['password    requisite     pam_pwquality.so minlen=8 usercheck=0\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened, persist=False)):
            S02204_pwordaccount()

        # Mock test setup.
        mock_add_bak_file.assert_called_once_with(SYSTEM_AUTH + '_bak')
        self.assertEqual(len(written), 1)
        self.assertEqual(written[0][0], SYSTEM_AUTH)
        mock_logger.warning.assert_called_once_with("set that the password does not contain the account string failed")
        mock_Display.assert_called_once_with(
            "- Set that the password does not contain the account string...", "FAILED")

    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.InsertSection')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.Display')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.logger')
    @patch('secScanner.enhance.euler.set.S02204_pwordaccount.seconf.get')
    def test_already_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_exists, mock_add_bak_file, mock_copy2):
        """边界：两个 PAM 文件均已启用 pam_pwquality.so 且无 usercheck=0 时不应重复写入"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        files = {
            SYSTEM_AUTH: ['password    requisite     pam_pwquality.so minlen=8 minclass=3\n'],
            PASSWORD_AUTH: ['password    requisite     pam_pwquality.so minlen=8 minclass=3\n'],
        }
        mock_exists.side_effect = _make_exists(files)
        written, opened = [], []

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(files, written, opened)):
            S02204_pwordaccount()

        # Mock test setup.
        self.assertEqual(written, [])
        mock_add_bak_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_logger.info.assert_called_once_with(
            "pam_pwquality is enabled without usercheck=0 in all PAM password stacks")
        mock_Display.assert_called_once_with(
            "- Already set that the password does not contain the account string...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
