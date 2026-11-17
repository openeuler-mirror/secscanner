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
from types import SimpleNamespace
from unittest.mock import patch, mock_open
import logging
import os
from secScanner.enhance.euler.set.S02209_grubpassword import S02209_grubpassword  # Mock test setup.

USER_CFG = os.path.join('/boot/grub2', 'user.cfg')

class TestS02209_grubpassword(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.secrets.token_urlsafe')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.subprocess.run')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.logger')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_token, mock_isdir):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02209_grubpassword()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_grubpassword')
        mock_InsertSection.assert_called_once_with("set grub password protection...")
        mock_isdir.assert_not_called()
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set grub password protection...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.chmod')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.secrets.token_urlsafe')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.subprocess.run')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.logger')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.seconf.get')
    @patch('builtins.open', new_callable=mock_open,
           read_data='GRUB2_PASSWORD=grub.pbkdf2.sha512.10000.OLDPASS\n')
    def test_set_password_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                   mock_run, mock_token, mock_isdir, mock_exists, mock_add_bak_file,
                                   mock_copy2, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        user_cfg_checked = {'count': 0}
        def fake_exists(path):
            if path.endswith('user.cfg'):
                user_cfg_checked['count'] += 1
                return user_cfg_checked['count'] > 1
            return False
        mock_exists.side_effect = fake_exists
        mock_token.return_value = 'mockpassword'
        mock_run.return_value = SimpleNamespace(
            returncode=0,
            stdout=b'grub.pbkdf2.sha512.10000.NEWHASH',
            stderr=b'')

        # Mock test setup.
        S02209_grubpassword()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_grubpassword')
        mock_InsertSection.assert_called_once_with("set grub password protection...")
        mock_token.assert_called_once_with(16)
        mock_run.assert_called_once()
        mock_file.assert_any_call(USER_CFG, 'r')
        mock_file.assert_any_call(USER_CFG, 'w')
        mock_file.assert_any_call('/root/grubpassword.txt', 'w')
        mock_copy2.assert_called_once_with(USER_CFG, USER_CFG + '_bak')
        mock_add_bak_file.assert_called_once_with(USER_CFG + '_bak')
        mock_chmod.assert_called_once_with('/root/grubpassword.txt', 0o600)
        mock_Display.assert_called_once_with(
            "- Set grub password protection, the password is saved in /root/grubpassword.txt...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02209_grubpassword.subprocess.run')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.secrets.token_urlsafe')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.logger')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.seconf.get')
    def test_generate_hash_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_token, mock_isdir, mock_exists, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        mock_exists.return_value = False
        mock_token.return_value = 'mockpassword'
        mock_run.return_value = SimpleNamespace(returncode=1, stdout=b'', stderr=b'failed')

        # Mock test setup.
        S02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set grub password protection...")
        mock_run.assert_called_once()
        mock_logger.warning.assert_called_once_with("generate the grub password hash failed")
        mock_Display.assert_called_once_with("- Generate the grub password hash...", "FAILED")

    @patch('secScanner.enhance.euler.set.S02209_grubpassword.subprocess.run')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.os.path.isdir')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.InsertSection')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.Display')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.logger')
    @patch('secScanner.enhance.euler.set.S02209_grubpassword.seconf.get')
    @patch('builtins.open', new_callable=mock_open,
           read_data='GRUB2_PASSWORD=grub.pbkdf2.sha512.10000.OLDPASS\n')
    def test_password_already_set_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                           mock_InsertSection, mock_isdir, mock_exists, mock_run):
        """边界：enable 但 user.cfg 中已存在 GRUB2_PASSWORD，应跳过不重新生成"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_isdir.side_effect = lambda path: path == '/boot/grub2'
        mock_exists.return_value = True

        # Mock test setup.
        S02209_grubpassword()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("set grub password protection...")
        mock_run.assert_not_called()
        mock_logger.info.assert_called_once_with("grub password is already set in user.cfg")
        mock_Display.assert_called_once_with("- Already set grub password protection...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
