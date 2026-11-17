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
from unittest.mock import patch
from secScanner.enhance.euler.set.S01114_keyfileperm import S01114_keyfileperm  # Mock test setup.

KEY_FILE_PERMS = {
    "/etc/passwd": "0644",
    "/etc/group": "0644",
    "/etc/shadow": "0000",
    "/etc/gshadow": "0000",
    "/etc/passwd-": "0644",
    "/etc/group-": "0644",
    "/etc/shadow-": "0000",
    "/etc/gshadow-": "0000",
    "/etc/ssh/sshd_config": "0600",
}

def _stat_with_perm(perm):
    return SimpleNamespace(st_mode=0o100000 | int(perm, 8))

class TestS01114_keyfileperm(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.chmod')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.logger')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_chmod, mock_stat):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01114_keyfileperm()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_keyfileperm')
        mock_InsertSection.assert_called_once_with("Set the permissions of the key files...")
        mock_exists.assert_not_called()
        mock_chmod.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set the permissions of the key files...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.chmod')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.logger')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.seconf.get')
    def test_set_permissions_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_chmod, mock_stat):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_stat.side_effect = lambda path: _stat_with_perm(KEY_FILE_PERMS[path])

        # Mock test setup.
        S01114_keyfileperm()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the permissions of the key files...")
        self.assertEqual(mock_chmod.call_count, len(KEY_FILE_PERMS))
        for keyFile, perm in KEY_FILE_PERMS.items():
            mock_chmod.assert_any_call(keyFile, int(perm, 8))
        mock_Display.assert_called_once_with("- Set the permissions of the key files...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.chmod')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.logger')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.seconf.get')
    def test_chmod_exception_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_chmod, mock_stat):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_chmod.side_effect = OSError("Permission denied")

        # Mock test setup.
        S01114_keyfileperm()

        # Mock test setup.
        mock_logger.warning.assert_any_call("Set the permission of %s failed", "/etc/passwd")
        mock_Display.assert_called_once_with("- Set the permissions of the key files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.chmod')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.logger')
    @patch('secScanner.enhance.euler.set.S01114_keyfileperm.seconf.get')
    def test_permission_verify_mismatch_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_chmod, mock_stat):
        """边界：chmod 未抛异常但复查权限仍不符，应判定 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_stat.side_effect = lambda path: _stat_with_perm(
            "0600" if path == "/etc/passwd" else KEY_FILE_PERMS[path])

        # Mock test setup.
        S01114_keyfileperm()

        # Mock test setup.
        mock_logger.warning.assert_any_call("Set the permission of %s failed", "/etc/passwd")
        mock_Display.assert_called_once_with("- Set the permissions of the key files...", "FAILED")

if __name__ == '__main__':
    unittest.main()
