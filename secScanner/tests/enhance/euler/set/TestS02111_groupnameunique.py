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
from secScanner.enhance.euler.set.S02111_groupnameunique import S02111_groupnameunique  # Mock test setup.

def _exists(path, group=True, bak=False):
    if path == '/etc/group':
        return group
    if path == '/etc/group_bak':
        return bak
    return False

class TestS02111_groupnameunique(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.logger')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02111_groupnameunique()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_groupnameunique')
        mock_InsertSection.assert_called_once_with("Ensure that the group name is unique")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- Skip ensure that the group name is unique due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.logger')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="root:x:0:\ndup:x:1000:\ndup:x:1001:\n")
    def test_remove_duplicate_group_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists

        # Mock test setup.
        S02111_groupnameunique()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Ensure that the group name is unique")
        mock_copy2.assert_called_once_with('/etc/group', '/etc/group_bak')
        mock_add_bak_file.assert_called_once_with('/etc/group_bak')
        mock_file.assert_any_call('/etc/group', 'r')
        mock_file.assert_any_call('/etc/group', 'w')
        mock_file().writelines.assert_called_once_with(['root:x:0:\n', 'dup:x:1000:\n'])
        mock_logger.info.assert_any_call("Remove the duplicate group name dup from /etc/group")
        mock_logger.info.assert_any_call("All duplicate group names have been removed from /etc/group.")
        mock_Display.assert_called_once_with("- All duplicate group names have been removed from /etc/group.", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.logger')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="root:x:0:\nbin:x:1:\n")
    def test_no_duplicate_group_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：无重复组名时不备份、不改写 /etc/group"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists

        # Mock test setup.
        S02111_groupnameunique()

        # Mock test setup.
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_called_once_with('/etc/group', 'r')
        mock_file().writelines.assert_not_called()
        mock_logger.info.assert_called_once_with("No duplicate group names found in /etc/group, no need to fix")
        mock_Display.assert_called_once_with("- No duplicate group names found in /etc/group...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.logger')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_group_file_missing(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：/etc/group 不存在时应 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: _exists(path, group=False)

        # Mock test setup.
        S02111_groupnameunique()

        # Mock test setup.
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("file /etc/group does not exist")
        mock_Display.assert_called_once_with("- file /etc/group not exists...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.InsertSection')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.Display')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.logger')
    @patch('secScanner.enhance.euler.set.S02111_groupnameunique.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="root:x:0:\ndup:x:1000:\ndup:x:1001:\n")
    def test_backup_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：备份文件失败时异常向上抛出，不应改写 /etc/group"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists
        mock_copy2.side_effect = OSError("backup failed")

        # Mock test setup.
        with self.assertRaises(OSError):
            S02111_groupnameunique()

        # Mock test setup.
        mock_add_bak_file.assert_not_called()
        mock_file.assert_called_once_with('/etc/group', 'r')
        mock_file().writelines.assert_not_called()

if __name__ == '__main__':
    unittest.main()
