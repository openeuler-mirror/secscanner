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
from unittest.mock import patch, MagicMock
from secScanner.enhance.euler.set.S02406_sudoersscript import S02406_sudoersscript  # Mock test setup.

SUDOERS_FILE = '/etc/sudoers'
SCRIPT_FILE = '/usr/local/bin/tool.sh'


def make_file(content=''):
    handle = MagicMock()
    handle.read.return_value = content
    handle.readlines.return_value = content.splitlines(True)
    handle.__iter__.return_value = iter(content.splitlines(True))
    handle.__enter__.return_value = handle
    file_mock = MagicMock()
    file_mock.__enter__.return_value = handle
    file_mock.__exit__.return_value = False
    return file_mock


def stat_info(mode, uid):
    info = MagicMock()
    info.st_mode = mode
    info.st_uid = uid
    return info


class TestS02406_sudoersscript(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.logger')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_exists, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02406_sudoersscript()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sudoersscript')
        mock_InsertSection.assert_called_once_with("set the scripts in sudoers not to be writable by low privilege users...")
        mock_Display.assert_called_once_with(
            "- Skip set the scripts in sudoers not to be writable by low privilege users...", "SKIPPING")
        mock_open.assert_not_called()
        mock_chmod.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.logger')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.seconf.get')
    def test_no_writable_script_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                         mock_open, mock_exists, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_open.return_value = make_file("%wheel ALL=(ALL) " + SCRIPT_FILE + "\n")
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SCRIPT_FILE)
        mock_stat.return_value = stat_info(0o755, 0)

        # Mock test setup.
        S02406_sudoersscript()

        # Mock test setup.
        mock_open.assert_called_once_with(SUDOERS_FILE, 'r')
        mock_chmod.assert_not_called()
        mock_logger.info.assert_called_once_with("no script in sudoers is writable by low privilege users")
        mock_Display.assert_called_once_with(
            "- Already set the scripts in sudoers not to be writable by low privilege users...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.logger')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.seconf.get')
    def test_chmod_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                    mock_open, mock_exists, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_open.return_value = make_file("%wheel ALL=(ALL) " + SCRIPT_FILE + "\n")
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SCRIPT_FILE)
        mock_stat.side_effect = [stat_info(0o777, 1000), stat_info(0o777, 1000), stat_info(0o555, 1000)]

        # Mock test setup.
        S02406_sudoersscript()

        # Mock test setup.
        mock_chmod.assert_called_once_with(SCRIPT_FILE, 0o555)
        mock_logger.info.assert_any_call(
            "remove the write permission of low privilege users from %s" % SCRIPT_FILE)
        mock_logger.info.assert_any_call(
            "set the scripts in sudoers not to be writable by low privilege users successfully")
        mock_Display.assert_called_once_with(
            "- Set the scripts in sudoers not to be writable by low privilege users...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.logger')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.seconf.get')
    def test_chmod_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                          mock_open, mock_exists, mock_stat, mock_chmod):
        """边界：chmod 后脚本仍可被低权限用户写入，应为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_open.return_value = make_file("%wheel ALL=(ALL) " + SCRIPT_FILE + "\n")
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SCRIPT_FILE)
        mock_stat.side_effect = [stat_info(0o777, 1000), stat_info(0o777, 1000), stat_info(0o777, 1000)]

        # Mock test setup.
        S02406_sudoersscript()

        # Mock test setup.
        mock_chmod.assert_called_once_with(SCRIPT_FILE, 0o555)
        mock_logger.warning.assert_called_once_with(
            "set the scripts in sudoers not to be writable by low privilege users failed")
        mock_Display.assert_called_once_with(
            "- Set the scripts in sudoers not to be writable by low privilege users...", "FAILED")

    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.stat')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.Display')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.logger')
    @patch('secScanner.enhance.euler.set.S02406_sudoersscript.seconf.get')
    def test_sudoers_missing_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                    mock_open, mock_exists, mock_stat, mock_chmod):
        """边界：/etc/sudoers 不存在时应为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S02406_sudoersscript()

        # Mock test setup.
        mock_open.assert_not_called()
        mock_chmod.assert_not_called()
        mock_logger.warning.assert_called_once_with("file /etc/sudoers does not exist")
        mock_Display.assert_called_once_with("- File /etc/sudoers does not exist...", "FAILED")


if __name__ == '__main__':
    unittest.main()
