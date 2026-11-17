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
from secScanner.enhance.euler.set.S01115_openfiles import S01115_openfiles  # Mock test setup.

class TestS01115_openfiles(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01115_openfiles.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.Display')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.logger')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01115_openfiles()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_openfiles')
        mock_InsertSection.assert_called_once_with("Set the open file limits in /etc/security/limits.conf...")
        mock_Display.assert_called_once_with("- Skip set the open file limits due to config file...", "SKIPPING")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S01115_openfiles.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.Display')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.logger')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="* soft nofile 2000\n* hard nofile 10000\n")
    def test_already_set_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_add_bak_file, mock_copy2):
        """边界：limits.conf 中已存在 * soft nofile 配置，应跳过写入"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S01115_openfiles()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_openfiles')
        mock_exists.assert_any_call('/etc/security/limits.conf')
        mock_add_bak_file.assert_called_once_with('/etc/security/limits.conf_bak')
        mock_copy2.assert_not_called()
        mock_logger.info.assert_called_once_with("The open file limits have already been set")
        mock_Display.assert_called_once_with("- The open file limits have already been set...", "SKIPPING")
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.set.S01115_openfiles.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.Display')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.logger')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        read_exist = mock_open(read_data="").return_value
        append_file = mock_open().return_value
        read_verify = mock_open(read_data="* soft nofile 2000\n* hard nofile 10000\n").return_value
        mock_file.side_effect = [read_exist, append_file, read_verify]

        # Mock test setup.
        S01115_openfiles()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_openfiles')
        mock_add_bak_file.assert_called_once_with('/etc/security/limits.conf_bak')
        mock_file.assert_any_call('/etc/security/limits.conf', 'a')
        append_file.write.assert_any_call("\n* soft nofile 2000\n")
        append_file.write.assert_any_call("* hard nofile 10000\n")
        mock_logger.info.assert_any_call("Set the open file limits finished, checking ok")
        mock_Display.assert_called_once_with("- Set the open file limits in limits.conf...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01115_openfiles.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.Display')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.logger')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        read_exist = mock_open(read_data="").return_value
        append_file = mock_open().return_value
        read_verify = mock_open(read_data="* soft nofile 1024\n").return_value
        mock_file.side_effect = [read_exist, append_file, read_verify]

        # Mock test setup.
        S01115_openfiles()

        # Mock test setup.
        mock_logger.warning.assert_called_once_with("Set the open file limits failed")
        mock_Display.assert_called_once_with("- Set the open file limits in limits.conf...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01115_openfiles.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.Display')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.logger')
    @patch('secScanner.enhance.euler.set.S01115_openfiles.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_missing_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_add_bak_file, mock_copy2):
        """边界：limits.conf 不存在，应直接失败且不读写文件"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S01115_openfiles()

        # Mock test setup.
        mock_logger.warning.assert_called_once_with("The config file /etc/security/limits.conf does not exist")
        mock_Display.assert_called_once_with("- The config file /etc/security/limits.conf does not exist...", "FAILED")
        mock_file.assert_not_called()
        mock_add_bak_file.assert_not_called()

if __name__ == '__main__':
    unittest.main()
