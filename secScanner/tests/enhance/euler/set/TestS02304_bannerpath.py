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
import secScanner.enhance.euler.set.S02304_bannerpath as S02304_module
from secScanner.enhance.euler.set.S02304_bannerpath import S02304_bannerpath  # Mock test setup.

CONFIG_FILE = '/etc/ssh/sshd_config'
BANNER_FILE = '/etc/issue.net'


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


def make_write_file(on_write):
    handle = MagicMock()
    handle.__enter__.return_value = handle
    handle.__exit__.return_value = False
    handle.write.side_effect = on_write
    return handle


class TestS02304_bannerpath(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S02304_bannerpath.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.chmod')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.logger')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                      mock_open, mock_exists, mock_chmod, mock_add_bak_file,
                                      mock_copy2, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S02304_bannerpath()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_bannerpath')
        mock_InsertSection.assert_called_once_with("set the banner path...")
        mock_Display.assert_called_once_with("- Skip set the banner path...", "SKIPPING")
        mock_open.assert_not_called()
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02304_bannerpath.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.chmod')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.logger')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.seconf.get')
    def test_banner_already_set_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                         mock_open, mock_exists, mock_chmod, mock_add_bak_file,
                                         mock_copy2, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_open.return_value = make_file("Port 22\nBanner %s\n" % BANNER_FILE)
        mock_exists.return_value = True

        # Mock test setup.
        S02304_bannerpath()

        # Mock test setup.
        mock_Display.assert_called_once_with("- Already set the banner path correctly...", "SKIPPING")
        mock_add_bak_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S02304_bannerpath.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.chmod')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.logger')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.seconf.get')
    def test_add_banner_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                 mock_open, mock_exists, mock_chmod, mock_add_bak_file,
                                 mock_copy2, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        state = {'config': "Port 22\n", 'truncated': False}
        issue = {'exists': False, 'content': ''}

        def _open(path, mode='r', *args, **kwargs):
            if path == CONFIG_FILE:
                if 'r' in mode:
                    return make_file(state['config'])
                def _write_config(data):
                    if mode.startswith('w') and not state['truncated']:
                        state['config'] = data
                        state['truncated'] = True
                    else:
                        state['config'] += data
                return make_write_file(_write_config)
            if path == BANNER_FILE and 'a' in mode:
                def _write_issue(data):
                    issue['content'] += data
                    issue['exists'] = True
                return make_write_file(_write_issue)
            raise AssertionError("unexpected open call: %s" % path)

        mock_open.side_effect = _open
        mock_exists.side_effect = lambda path: path in (CONFIG_FILE, CONFIG_FILE + '_bak') or (
            path == BANNER_FILE and issue['exists'])
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S02304_bannerpath()

        # Mock test setup.
        mock_add_bak_file.assert_called_once_with(CONFIG_FILE + '_bak')
        mock_copy2.assert_not_called()
        mock_getstatusoutput.assert_called_once_with('systemctl restart sshd')
        mock_chmod.assert_called_once_with(BANNER_FILE, 0o644)
        self.assertIn('\nBanner %s\n' % BANNER_FILE, state['config'])
        self.assertIn('Authorized users only', issue['content'])
        mock_logger.info.assert_any_call("set the banner path successfully")
        mock_Display.assert_called_once_with("- Set the banner path...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S02304_bannerpath.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.add_bak_file')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.chmod')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.os.path.exists')
    @patch('builtins.open')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.InsertSection')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.Display')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.logger')
    @patch('secScanner.enhance.euler.set.S02304_bannerpath.seconf.get')
    def test_sshd_config_missing_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                        mock_open, mock_exists, mock_chmod, mock_add_bak_file,
                                        mock_copy2, mock_getstatusoutput):
        """边界：sshd_config 不存在时应为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S02304_bannerpath()

        # Mock test setup.
        mock_logger.warning.assert_called_once_with("file /etc/ssh/sshd_config does not exist")
        mock_Display.assert_called_once_with("- File /etc/ssh/sshd_config does not exist...", "FAILED")
        mock_open.assert_not_called()
        mock_getstatusoutput.assert_not_called()


if __name__ == '__main__':
    unittest.main()
