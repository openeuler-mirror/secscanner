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
from secScanner.enhance.euler.check.C02111_groupnameunique import C02111_groupnameunique  # Mock test setup.

def _exists(path, group=True):
    if path == '/etc/group':
        return group
    return False

class TestC02111_groupnameunique(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.read_group_file')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_duplicate_group_name_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_group_file):
        # Mock test setup.
        mock_read_group_file.return_value = [
            'root:x:0:\n',
            'dup:x:1000:\n',
            'dup:x:1001:\n',
        ]
        mock_exists.side_effect = _exists

        # Mock test setup.
        secScanner.enhance.euler.check.C02111_groupnameunique.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02111_groupnameunique()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check if the group name is unique")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC02111\n")
        mock_logger.warning.assert_any_call("WRN_C02111: %s", WRN_C02111)
        mock_logger.warning.assert_any_call("SUG_C02111: %s", SUG_C02111)
        mock_Display.assert_any_call("- Duplicate group names found in /etc/group ...", "WARNING")

    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.read_group_file')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_group_name_unique_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_group_file):
        # Mock test setup.
        mock_read_group_file.return_value = [
            'root:x:0:\n',
            'bin:x:1:\n',
            'secscanner:x:1000:\n',
        ]
        mock_exists.side_effect = _exists

        # Mock test setup.
        secScanner.enhance.euler.check.C02111_groupnameunique.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02111_groupnameunique()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check if the group name is unique")
        mock_file.assert_not_called()
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("No duplicate group names found in /etc/group, checking ok")
        mock_Display.assert_called_once_with("- No duplicate group names found in /etc/group...", "OK")

    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.read_group_file')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.check.C02111_groupnameunique.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_group_file_missing(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_read_group_file):
        """边界：/etc/group 不存在时应 SKIPPING 并写入 RESULT_FILE"""
        # Mock test setup.
        mock_exists.side_effect = lambda path: _exists(path, group=False)

        # Mock test setup.
        secScanner.enhance.euler.check.C02111_groupnameunique.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C02111_groupnameunique()

        # Mock test setup.
        mock_read_group_file.assert_not_called()
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC02111\n")
        mock_logger.warning.assert_any_call("WRN_C02111: /etc/group %s" % WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C02111: /etc/group %s" % SUG_no_file)
        mock_Display.assert_called_once_with("- file /etc/group does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
