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
from secScanner.enhance.euler.set.S01105_umask import S01105_umask  # Mock test setup.

def _file_handle(lines):
    handle = mock_open()()
    handle.readlines.return_value = lines
    return handle

class TestS01105_umask(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01105_umask.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01105_umask.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.set.S01105_umask.Display')
    @patch('secScanner.enhance.euler.set.S01105_umask.logger')
    @patch('secScanner.enhance.euler.set.S01105_umask.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak):
        # Mock test setup.
        mock_seconf_get.side_effect = ['no', '027']

        # Mock test setup.
        S01105_umask()

        # Mock test setup.
        mock_seconf_get.assert_any_call('euler', 'set_umask')
        mock_seconf_get.assert_any_call('euler', 'umask_value')
        mock_InsertSection.assert_called_once_with("Set the UMASK in /etc/bashrc...")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set the UMASK due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01105_umask.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01105_umask.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.set.S01105_umask.Display')
    @patch('secScanner.enhance.euler.set.S01105_umask.logger')
    @patch('secScanner.enhance.euler.set.S01105_umask.seconf.get')
    def test_config_file_missing_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak):
        """边界：/etc/bashrc 不存在，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', '027']
        mock_exists.return_value = False

        # Mock test setup.
        S01105_umask()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the UMASK in /etc/bashrc...")
        mock_copy2.assert_not_called()
        mock_logger.warning.assert_called_once_with("The config file /etc/bashrc does not exist")
        mock_Display.assert_called_once_with("- The config file /etc/bashrc does not exist...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01105_umask.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01105_umask.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.set.S01105_umask.Display')
    @patch('secScanner.enhance.euler.set.S01105_umask.logger')
    @patch('secScanner.enhance.euler.set.S01105_umask.seconf.get')
    def test_replace_existing_umask_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak):
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', '027']
        mock_exists.side_effect = [True, False]
        handles = [_file_handle(['# bashrc\n', 'umask 022\n']), _file_handle([]), _file_handle(['# bashrc\n', 'umask 027\n'])]

        # Mock test setup.
        with patch('builtins.open', side_effect=handles):
            S01105_umask()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the UMASK in /etc/bashrc...")
        mock_copy2.assert_called_once_with('/etc/bashrc', '/etc/bashrc_bak')
        mock_add_bak.assert_called_once_with('/etc/bashrc_bak')
        handles[1].write.assert_any_call("umask 027\n")
        mock_logger.info.assert_called_once_with("Set the UMASK finished, checking ok")
        mock_Display.assert_called_once_with("- Set the UMASK in /etc/bashrc...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01105_umask.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01105_umask.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.set.S01105_umask.Display')
    @patch('secScanner.enhance.euler.set.S01105_umask.logger')
    @patch('secScanner.enhance.euler.set.S01105_umask.seconf.get')
    def test_append_umask_when_missing_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak):
        """边界：文件中无 umask 行，应追加配置并校验通过"""
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', '027']
        mock_exists.side_effect = [True, True]
        handles = [_file_handle(['# bashrc\n']), _file_handle([]), _file_handle(['# bashrc\n', 'umask 027\n'])]

        # Mock test setup.
        with patch('builtins.open', side_effect=handles):
            S01105_umask()

        # Mock test setup.
        mock_copy2.assert_not_called()
        mock_add_bak.assert_called_once_with('/etc/bashrc_bak')
        handles[1].write.assert_called_once_with("\numask 027\n")
        mock_Display.assert_called_once_with("- Set the UMASK in /etc/bashrc...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01105_umask.add_bak_file')
    @patch('secScanner.enhance.euler.set.S01105_umask.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.set.S01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.set.S01105_umask.Display')
    @patch('secScanner.enhance.euler.set.S01105_umask.logger')
    @patch('secScanner.enhance.euler.set.S01105_umask.seconf.get')
    def test_umask_check_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_copy2, mock_add_bak):
        """边界：回读校验值不一致，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.side_effect = ['yes', '027']
        mock_exists.return_value = True
        handles = [_file_handle(['umask 077\n']), _file_handle([]), _file_handle(['umask 077\n'])]

        # Mock test setup.
        with patch('builtins.open', side_effect=handles):
            S01105_umask()

        # Mock test setup.
        mock_logger.warning.assert_called_once_with("Set the UMASK failed")
        mock_Display.assert_called_once_with("- Set the UMASK in /etc/bashrc...", "FAILED")

if __name__ == '__main__':
    unittest.main()
