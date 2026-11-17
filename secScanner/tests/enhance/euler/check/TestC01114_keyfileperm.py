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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01114_keyfileperm import C01114_keyfileperm  # Mock test setup.

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

class TestC01114_keyfileperm(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_wrong_permission_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_stat):
        # Mock test setup.
        mock_exists.side_effect = lambda path: path == "/etc/passwd"
        mock_stat.return_value = _stat_with_perm("0666")

        # Mock test setup.
        secScanner.enhance.euler.check.C01114_keyfileperm.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01114_keyfileperm()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the permissions of the key files are minimized")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01114\n")
        mock_logger.warning.assert_any_call("WRN_C01114_%02d: %s", 1, WRN_C01114_01)
        mock_logger.warning.assert_any_call("SUG_C01114_%02d: %s", 1, SUG_C01114_01)
        mock_Display.assert_called_once_with("- The permission of /etc/passwd is not safe...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_all_permissions_safe(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_stat):
        # Mock test setup.
        mock_exists.return_value = True
        mock_stat.side_effect = lambda path: _stat_with_perm(KEY_FILE_PERMS[path])

        # Mock test setup.
        C01114_keyfileperm()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the permissions of the key files are minimized")
        mock_file().write.assert_not_called()
        self.assertEqual(mock_Display.call_count, len(KEY_FILE_PERMS))
        for keyFile in KEY_FILE_PERMS:
            mock_Display.assert_any_call("- Check the permission of %s..." % keyFile, "OK")

    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.stat')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.InsertSection')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.Display')
    @patch('secScanner.enhance.euler.check.C01114_keyfileperm.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_shadow_group_readable_boundary(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_stat):
        """边界：/etc/shadow 仅组可读（0400）也属于不合规，应触发 WARNING"""
        # Mock test setup.
        mock_exists.side_effect = lambda path: path == "/etc/shadow"
        mock_stat.return_value = _stat_with_perm("0400")

        # Mock test setup.
        secScanner.enhance.euler.check.C01114_keyfileperm.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01114_keyfileperm()

        # Mock test setup.
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01114\n")
        mock_logger.warning.assert_any_call("WRN_C01114_%02d: %s", 3, WRN_C01114_03)
        mock_Display.assert_called_once_with("- The permission of /etc/shadow is not safe...", "WARNING")

if __name__ == '__main__':
    unittest.main()
