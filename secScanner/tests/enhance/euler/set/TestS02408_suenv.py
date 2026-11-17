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
from secScanner.enhance.euler.set.S02408_suenv import S02408_suenv

CONFIG_FILE = '/etc/login.defs'


def _make_open(state, written, opened):
    def _open(path, mode="r", *args, **kwargs):
        opened.append((path, mode, kwargs.get("encoding")))
        handle = MagicMock()
        handle.__enter__.return_value = handle
        handle.__exit__.return_value = False
        if "r" in mode:
            handle.readlines.return_value = list(state.get(path, []))
            return handle
        if "a" in mode:
            def _append(data):
                state.setdefault(path, []).extend(data.splitlines(True))
                written.append((path, data))
            handle.write.side_effect = _append
            return handle
        buffer = []

        def _write(data):
            buffer.append(data)
            written.append((path, data))

        def _close(*args):
            state[path] = buffer
            return False

        handle.write.side_effect = _write
        handle.__exit__.side_effect = _close
        return handle
    return _open


class TestS02408_suenv(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02408_suenv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02408_suenv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02408_suenv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02408_suenv.Display')
    @patch('secScanner.enhance.euler.set.S02408_suenv.logger')
    @patch('secScanner.enhance.euler.set.S02408_suenv.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02408_suenv()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_suenv')
        mock_InsertSection.assert_called_once_with("set su command not to inherit the user PATH environment variable...")
        mock_Display.assert_called_once_with("- Skip set su command not to inherit the user PATH environment variable...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02408_suenv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02408_suenv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02408_suenv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02408_suenv.Display')
    @patch('secScanner.enhance.euler.set.S02408_suenv.logger')
    @patch('secScanner.enhance.euler.set.S02408_suenv.seconf.get')
    def test_add_always_set_path_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                          mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {CONFIG_FILE: ['PASS_MAX_DAYS\t99999\n']}
        written, opened = [], []
        mock_exists.side_effect = lambda path: path == CONFIG_FILE

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(state, written, opened)):
            S02408_suenv()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_suenv')
        mock_copy2.assert_called_once_with(CONFIG_FILE, CONFIG_FILE + '_bak')
        mock_add_bak_file.assert_called_once_with(CONFIG_FILE + '_bak')
        self.assertIn(('ALWAYS_SET_PATH\t\tyes\n'), state[CONFIG_FILE])
        self.assertIn((CONFIG_FILE, '\nALWAYS_SET_PATH\t\tyes\n'), written)
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Set ALWAYS_SET_PATH=yes in /etc/login.defs...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02408_suenv.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02408_suenv.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02408_suenv.os.path.exists')
    @patch('secScanner.enhance.euler.set.S02408_suenv.InsertSection')
    @patch('secScanner.enhance.euler.set.S02408_suenv.Display')
    @patch('secScanner.enhance.euler.set.S02408_suenv.logger')
    @patch('secScanner.enhance.euler.set.S02408_suenv.seconf.get')
    def test_login_defs_missing_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                       mock_exists, mock_add_bak_file, mock_copy2):
        """边界：/etc/login.defs 不存在时应返回 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S02408_suenv()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_suenv')
        mock_logger.warning.assert_called_once_with("file /etc/login.defs does not exist")
        mock_Display.assert_called_once_with("- File /etc/login.defs does not exist...", "FAILED")
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()


if __name__ == '__main__':
    unittest.main()
