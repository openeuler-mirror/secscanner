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
import logging
from secScanner.enhance.euler.set.S03309_permitrootlogin import S03309_permitrootlogin  # Mock test setup.

CONFIG_FILE = "/etc/ssh/sshd_config"
BAK_FILE = "/etc/ssh/sshd_config_bak"
SECTION = "Set config of PermitRootLogin..."

class TestS03309_permitrootlogin(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.logger')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03309_permitrootlogin()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_permitrootlogin')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_Display.assert_called_once_with("Skip set PermitRootLogin due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.logger')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="PermitRootLogin no\n")
    def test_already_right_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                    mock_InsertSection, mock_add_bak_file, mock_copy2, mock_exists):
        """边界：已存在正确的 PermitRootLogin no 且备份文件已存在，不再复制备份"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]

        # Mock test setup.
        S03309_permitrootlogin()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_permitrootlogin')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_logger.info.assert_called_once_with("Check set of PermitRootLogin right")
        mock_Display.assert_called_once_with("- Already right set PermitRootLogin in sshd config", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.logger')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_permit_root_login_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                            mock_InsertSection, mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]
        read_handle = mock_open(read_data="# config\nPermitRootLogin yes\n")()
        write_handle = mock_open()()
        verify_handle = mock_open(read_data="PermitRootLogin no\n")()
        mock_file.side_effect = [read_handle, write_handle, verify_handle]

        # Mock test setup.
        S03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_copy2.assert_called_once_with(CONFIG_FILE, BAK_FILE)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        write_handle.write.assert_any_call("# config\n")
        write_handle.write.assert_any_call("PermitRootLogin no\n")
        mock_logger.info.assert_called_once_with("Set PermitRootLogin finish")
        mock_Display.assert_called_once_with("- Set PermitRootLogin no in sshd config and restart sshd service", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.logger')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_verify_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                           mock_InsertSection, mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]
        read_handle = mock_open(read_data="PermitRootLogin yes\n")()
        write_handle = mock_open()()
        verify_handle = mock_open(read_data="PermitRootLogin yes\n")()
        mock_file.side_effect = [read_handle, write_handle, verify_handle]

        # Mock test setup.
        S03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_logger.warning.assert_called_once_with("Set PermitRootLogin failed")
        mock_Display.assert_called_once_with("- Set PermitRootLogin in sshd config", "FAILED")

    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.InsertSection')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.Display')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.logger')
    @patch('secScanner.enhance.euler.set.S03309_permitrootlogin.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                          mock_InsertSection, mock_add_bak_file, mock_copy2, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S03309_permitrootlogin()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_logger.warning.assert_called_once_with("sshd config file not exist")
        mock_Display.assert_called_once_with("- sshd config file not exist", "FAILED")

if __name__ == '__main__':
    unittest.main()
