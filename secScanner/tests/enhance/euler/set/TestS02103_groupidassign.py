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
from secScanner.enhance.euler.set.S02103_groupidassign import S02103_groupidassign  # Mock test setup.

def _exists(path, login_defs=True, bak=False):
    if path == '/etc/login.defs':
        return login_defs
    if path == '/etc/login.defs_bak':
        return bak
    return False

class TestS02103_groupidassign(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02103_groupidassign.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.logger')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02103_groupidassign()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_groupidassign')
        mock_InsertSection.assert_called_once_with("Ensure different accounts are assigned different group IDs...")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- Skip ensure different accounts are assigned different group IDs due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02103_groupidassign.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.logger')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB no\n")
    def test_set_usergroups_enab_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists

        # Mock test setup.
        S02103_groupidassign()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Ensure different accounts are assigned different group IDs...")
        mock_copy2.assert_called_once_with('/etc/login.defs', '/etc/login.defs_bak')
        mock_add_bak_file.assert_called_once_with('/etc/login.defs_bak')
        mock_file.assert_any_call('/etc/login.defs', 'r')
        mock_file.assert_any_call('/etc/login.defs', 'w')
        mock_file().writelines.assert_called_once_with(['USERGROUPS_ENAB yes\n'])
        mock_logger.info.assert_any_call("Set USERGROUPS_ENAB to yes in /etc/login.defs, checking ok")
        mock_Display.assert_called_once_with("- Set USERGROUPS_ENAB to yes in /etc/login.defs...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02103_groupidassign.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.logger')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB yes\n")
    def test_already_enabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：USERGROUPS_ENAB 已为 yes，不应备份或改写文件"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists

        # Mock test setup.
        S02103_groupidassign()

        # Mock test setup.
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_called_once_with('/etc/login.defs', 'r')
        mock_file().writelines.assert_not_called()
        mock_logger.info.assert_called_once_with("USERGROUPS_ENAB is already set to yes in /etc/login.defs")
        mock_Display.assert_called_once_with("- USERGROUPS_ENAB is already set to yes...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02103_groupidassign.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.logger')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_login_defs_missing(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：/etc/login.defs 不存在时应 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = lambda path: _exists(path, login_defs=False)

        # Mock test setup.
        S02103_groupidassign()

        # Mock test setup.
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("file /etc/login.defs does not exist")
        mock_Display.assert_called_once_with("- file /etc/login.defs not exists...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02103_groupidassign.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.InsertSection')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.Display')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.logger')
    @patch('secScanner.enhance.euler.set.S02103_groupidassign.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="USERGROUPS_ENAB no\n")
    def test_backup_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：备份文件失败时异常向上抛出，不应改写 /etc/login.defs"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = _exists
        mock_copy2.side_effect = OSError("backup failed")

        # Mock test setup.
        with self.assertRaises(OSError):
            S02103_groupidassign()

        # Mock test setup.
        mock_add_bak_file.assert_not_called()
        mock_file.assert_any_call('/etc/login.defs', 'r')
        mock_file.assert_called_once_with('/etc/login.defs', 'r')
        mock_file().writelines.assert_not_called()

if __name__ == '__main__':
    unittest.main()
