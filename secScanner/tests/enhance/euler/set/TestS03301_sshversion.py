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
from secScanner.enhance.euler.set.S03301_sshversion import S03301_sshversion

CONFIG_FILE = '/etc/ssh/sshd_config'


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


class TestS03301_sshversion(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03301_sshversion.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.InsertSection')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.Display')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.logger')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03301_sshversion()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshversion')
        mock_InsertSection.assert_called_once_with("Set config of ssh protocol version...")
        mock_Display.assert_called_once_with("Skip set ssh protocol version due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S03301_sshversion.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.InsertSection')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.Display')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.logger')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.seconf.get')
    def test_add_protocol_2_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                     mock_exists, mock_add_bak_file, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {CONFIG_FILE: ['Port 22\n']}
        written, opened = [], []
        mock_exists.side_effect = lambda path: path == CONFIG_FILE

        # Mock test setup.
        with patch('builtins.open', side_effect=_make_open(state, written, opened)):
            S03301_sshversion()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshversion')
        mock_copy2.assert_called_once_with(CONFIG_FILE, CONFIG_FILE + '_bak')
        mock_add_bak_file.assert_called_once_with(CONFIG_FILE + '_bak')
        self.assertIn('Protocol 2\n', state[CONFIG_FILE])
        self.assertIn((CONFIG_FILE, '\nProtocol 2\n'), written)
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Set Protocol 2 in sshd config and restart sshd service", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03301_sshversion.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.add_bak_file')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.InsertSection')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.Display')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.logger')
    @patch('secScanner.enhance.euler.set.S03301_sshversion.seconf.get')
    def test_sshd_config_missing_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                        mock_exists, mock_add_bak_file, mock_copy2):
        """边界：sshd_config 不存在时应返回 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S03301_sshversion()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_sshversion')
        mock_logger.warning.assert_called_once_with("sshd config file not exist")
        mock_Display.assert_called_once_with("- sshd config file not exist", "FAILED")
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()


if __name__ == '__main__':
    unittest.main()
