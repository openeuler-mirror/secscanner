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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C02103_groupidassign import C02103_groupidassign  # Mock test setup.

def _exists(path, passwd=True, login_defs=True):
    if path == '/etc/passwd':
        return passwd
    if path == '/etc/login.defs':
        return login_defs
    return False

class TestC02103_groupidassign(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02103_groupidassign.read_passwd_file')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB yes\n")
    def test_duplicate_gid_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_passwd_file):
        # Mock test setup.
        mock_read_passwd_file.return_value = [
            'root:x:0:0:root:/root:/bin/bash\n',
            'user1:x:1000:1000::/home/user1:/bin/bash\n',
            'user2:x:1001:1000::/home/user2:/bin/bash\n',
        ]
        mock_exists.side_effect = _exists

        # Mock test setup.
        secScanner.enhance.euler.check.C02103_groupidassign.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02103_groupidassign()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether different accounts are assigned different group IDs")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC02103\n")
        mock_logger.warning.assert_any_call("WRN_C02103_01: %s", WRN_C02103_01)
        mock_logger.warning.assert_any_call("SUG_C02103_01: %s", SUG_C02103_01)
        mock_Display.assert_any_call("- Duplicate group IDs found in /etc/passwd ...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02103_groupidassign.read_passwd_file')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB yes\n")
    def test_no_duplicate_gid_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_passwd_file):
        # Mock test setup.
        mock_read_passwd_file.return_value = [
            'root:x:0:0:root:/root:/bin/bash\n',
            'user1:x:1000:1000::/home/user1:/bin/bash\n',
            'user2:x:1001:1001::/home/user2:/bin/bash\n',
        ]
        mock_exists.side_effect = _exists

        # Mock test setup.
        secScanner.enhance.euler.check.C02103_groupidassign.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02103_groupidassign()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether different accounts are assigned different group IDs")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_any_call("No duplicate group IDs found in /etc/passwd, checking ok")
        mock_logger.info.assert_any_call("USERGROUPS_ENAB is set to yes in /etc/login.defs, checking ok")
        mock_Display.assert_any_call("- No duplicate group IDs found in /etc/passwd...", "OK")
        mock_Display.assert_any_call("- Check the USERGROUPS_ENAB is set to yes in /etc/login.defs...", "OK")

    @patch('secScanner.enhance.euler.check.C02103_groupidassign.read_passwd_file')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB no\n")
    def test_gid_zero_excluded_and_usergroups_disabled(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_passwd_file):
        """边界：gid 为 0 的重复项应被排除，仅 USERGROUPS_ENAB 未开启产生告警"""
        # Mock test setup.
        mock_read_passwd_file.return_value = [
            'root:x:0:0:root:/root:/bin/bash\n',
            'root2:x:0:0::/root2:/bin/bash\n',
            'user1:x:1000:1000::/home/user1:/bin/bash\n',
            'user2:x:1001:1001::/home/user2:/bin/bash\n',
        ]
        mock_exists.side_effect = _exists

        # Mock test setup.
        secScanner.enhance.euler.check.C02103_groupidassign.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02103_groupidassign()

        # Mock test setup.
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC02103\n")
        mock_Display.assert_any_call("- No duplicate group IDs found in /etc/passwd...", "OK")
        mock_Display.assert_any_call("- Check the USERGROUPS_ENAB is not set to yes in /etc/login.defs...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C02103_02: %s", WRN_C02103_02)
        mock_logger.warning.assert_any_call("SUG_C02103_02: %s", SUG_C02103_02)
        self.assertEqual(mock_logger.warning.call_count, 2)

    @patch('secScanner.enhance.euler.check.C02103_groupidassign.read_passwd_file')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.check.C02103_groupidassign.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_passwd_and_login_defs_missing(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_passwd_file):
        """边界：/etc/passwd 与 /etc/login.defs 均不存在，应各自 SKIPPING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_exists.side_effect = lambda path: _exists(path, passwd=False, login_defs=False)

        # Mock test setup.
        secScanner.enhance.euler.check.C02103_groupidassign.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02103_groupidassign()

        # Mock test setup.
        mock_read_passwd_file.assert_not_called()
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_logger.warning.assert_any_call("WRN_C02103: /etc/passwd %s" % WRN_no_file)
        mock_logger.warning.assert_any_call("WRN_C02103: /etc/login.defs %s" % WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02103: /etc/passwd %s" % SUG_no_file)
        mock_logger.warning.assert_any_call("SUG_C02103: /etc/login.defs %s" % SUG_no_file)
        mock_Display.assert_any_call("- file /etc/passwd does not exist...", "SKIPPING")
        mock_Display.assert_any_call("- file /etc/login.defs does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
