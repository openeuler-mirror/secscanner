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
from secScanner.enhance.euler.set.S03308_sshcryptooverride import S03308_sshcryptooverride  # Mock test setup.

CONFIG_FILE = '/etc/sysconfig/sshd'
BAK_FILE = '/etc/sysconfig/sshd_bak'
SECTION = "Set config of sshd crypto policy override..."

class TestS03308_sshcryptooverride(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.logger')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03308_sshcryptooverride()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshcryptooverride')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("Skip set sshd crypto policy override due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.logger')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="# nothing here\n")
    def test_no_override_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        """边界：已无 CRYPTO_POLICY 覆盖，无需改写应直接 FINISHED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]

        # Mock test setup.
        S03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_copy2.assert_not_called()
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("Check crypto policy override of sshd right")
        mock_Display.assert_called_once_with("- Already no crypto policy override in /etc/sysconfig/sshd", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.logger')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_comment_override_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]
        mock_file().readlines.side_effect = [
            ["CRYPTO_POLICY=DEFAULT\n"],
            ["# CRYPTO_POLICY=DEFAULT\n"],
        ]

        # Mock test setup.
        S03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_file.assert_any_call(CONFIG_FILE, "w")
        mock_file().write.assert_called_once_with("# CRYPTO_POLICY=DEFAULT\n")
        mock_logger.info.assert_called_once_with("Remove crypto policy override of sshd finish")
        mock_Display.assert_called_once_with("- Comment crypto policy override in /etc/sysconfig/sshd and reload sshd service", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.InsertSection')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.Display')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.logger')
    @patch('secScanner.enhance.euler.set.S03308_sshcryptooverride.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_remove_override_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]
        mock_file().readlines.side_effect = [
            ["CRYPTO_POLICY=DEFAULT\n"],
            ["CRYPTO_POLICY=DEFAULT\n"],
        ]

        # Mock test setup.
        S03308_sshcryptooverride()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_logger.warning.assert_called_once_with("Remove crypto policy override of sshd failed")
        mock_Display.assert_called_once_with("- Remove crypto policy override in /etc/sysconfig/sshd", "FAILED")

if __name__ == '__main__':
    unittest.main()
