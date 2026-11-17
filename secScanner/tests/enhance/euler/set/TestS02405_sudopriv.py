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
import secScanner.enhance.euler.set.S02405_sudopriv as S02405_module
from secScanner.enhance.euler.set.S02405_sudopriv import S02405_sudopriv  # Mock test setup.

SUDOERS_FILE = '/etc/sudoers'
SUDOERS_BAK = '/etc/sudoers_bak'


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


def make_write_file(on_writelines=None):
    handle = MagicMock()
    handle.__enter__.return_value = handle
    handle.__exit__.return_value = False
    if on_writelines is not None:
        handle.writelines.side_effect = on_writelines
    return handle


def make_sudoers_router(state):
    def _open(path, mode='r', *args, **kwargs):
        if path != SUDOERS_FILE:
            raise AssertionError("unexpected open call: %s" % path)
        if 'r' in mode:
            return make_file(state['content'])

        def _write_lines(lines):
            state['content'] = ''.join(lines)
        return make_write_file(_write_lines)
    return _open


class TestS02405_sudopriv(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.logger')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_exists, mock_add_bak_file, mock_copy2,
                                      mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02405_sudopriv()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sudopriv')
        mock_InsertSection.assert_called_once_with("set normal users to run privileged programs through sudo...")
        mock_Display.assert_called_once_with(
            "- Skip set normal users to run privileged programs through sudo...", "SKIPPING")
        mock_open.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.logger')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.seconf.get')
    def test_add_wheel_rule_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                     mock_open, mock_exists, mock_add_bak_file, mock_copy2,
                                     mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {'content': "Defaults env_reset\nroot ALL=(ALL) ALL\n"}
        mock_open.side_effect = make_sudoers_router(state)
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SUDOERS_BAK)
        mock_getstatusoutput.side_effect = [(0, 'sudo-1.9.5p2-1.oe2203'), (0, 'parsed OK')]

        # Mock test setup.
        S02405_sudopriv()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sudopriv')
        mock_InsertSection.assert_called_once_with("set normal users to run privileged programs through sudo...")
        mock_add_bak_file.assert_called_once_with(SUDOERS_BAK)
        mock_copy2.assert_not_called()
        mock_getstatusoutput.assert_any_call('rpm -q sudo')
        mock_getstatusoutput.assert_any_call('visudo -c')
        self.assertIn('%wheel', state['content'])
        mock_logger.info.assert_any_call("set normal users to run privileged programs through sudo successfully")
        mock_Display.assert_called_once_with(
            "- Set normal users to run privileged programs through sudo...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.logger')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.seconf.get')
    def test_visudo_check_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                 mock_open, mock_exists, mock_add_bak_file, mock_copy2,
                                 mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {'content': "Defaults env_reset\nroot ALL=(ALL) ALL\n"}
        mock_open.side_effect = make_sudoers_router(state)
        mock_exists.side_effect = lambda path: path in (SUDOERS_FILE, SUDOERS_BAK)
        mock_getstatusoutput.side_effect = [(0, 'sudo-1.9.5p2-1.oe2203'), (1, 'syntax error')]

        # Mock test setup.
        S02405_sudopriv()

        # Mock test setup.
        mock_add_bak_file.assert_called_once_with(SUDOERS_BAK)
        mock_copy2.assert_called_once_with(SUDOERS_BAK, SUDOERS_FILE)
        mock_logger.warning.assert_any_call("visudo check failed: syntax error")
        mock_Display.assert_called_once_with(
            "- Set normal users to run privileged programs through sudo...", "FAILED")

    @patch('secScanner.enhance.euler.set.S02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.logger')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.seconf.get')
    def test_already_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_open, mock_exists, mock_add_bak_file, mock_copy2,
                                  mock_getstatusoutput):
        """边界：root 与 wheel 规则均已配置，不应修改文件"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {'content': "root ALL=(ALL) ALL\n%wheel ALL=(ALL) ALL\n"}
        mock_open.side_effect = make_sudoers_router(state)
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, 'sudo-1.9.5p2-1.oe2203')

        # Mock test setup.
        S02405_sudopriv()

        # Mock test setup.
        mock_open.assert_called_once_with(SUDOERS_FILE, 'r')
        mock_add_bak_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_getstatusoutput.assert_called_once_with('rpm -q sudo')
        mock_logger.info.assert_called_once_with("sudo rule is already set for normal users")
        mock_Display.assert_called_once_with(
            "- Already set normal users to run privileged programs through sudo...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S02405_sudopriv.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.Display')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.logger')
    @patch('secScanner.enhance.euler.set.S02405_sudopriv.seconf.get')
    def test_sudo_not_installed_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_open, mock_exists, mock_add_bak_file, mock_copy2,
                                       mock_getstatusoutput):
        """边界：未安装 sudo 时应为 FAILED 且不修改配置"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (1, 'package sudo is not installed')

        # Mock test setup.
        S02405_sudopriv()

        # Mock test setup.
        mock_open.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_logger.warning.assert_called_once_with("sudo is not installed, please install it manually")
        mock_Display.assert_called_once_with(
            "- sudo is not installed, please install it manually...", "FAILED")


if __name__ == '__main__':
    unittest.main()
