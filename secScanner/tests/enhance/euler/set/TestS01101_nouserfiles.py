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
from unittest.mock import patch
import logging
from secScanner.enhance.euler.set.S01101_nouserfiles import S01101_nouserfiles  # Mock test setup.

class TestS01101_nouserfiles(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.logger')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01101_nouserfiles()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_nouserfiles')
        mock_InsertSection.assert_called_once_with("Set the owner and group of the files or directories without owner or group...")
        mock_Display.assert_called_once_with("- Skip set the owner and group of the files or directories...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.logger')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.seconf.get')
    def test_no_files_found_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：find 两次均无结果，未执行 chown，应视为 FINISHED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, ''), (0, '')]

        # Mock test setup.
        S01101_nouserfiles()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_nouserfiles')
        mock_InsertSection.assert_called_once_with("Set the owner and group of the files or directories without owner or group...")
        self.assertEqual(mock_getstatusoutput.call_count, 2)
        mock_Display.assert_called_once_with("- Set the owner and group of the files or directories...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.logger')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.seconf.get')
    def test_chown_all_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, '/tmp/orphan_file\n/tmp/orphan_dir'), (0, ''), (0, ''), (0, '')]

        # Mock test setup.
        S01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the owner and group of the files or directories without owner or group...")
        self.assertEqual(mock_getstatusoutput.call_count, 4)
        mock_getstatusoutput.assert_any_call('chown root:root "/tmp/orphan_file"')
        mock_getstatusoutput.assert_any_call('chown root:root "/tmp/orphan_dir"')
        mock_Display.assert_called_once_with("- Set the owner and group of the files or directories...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.logger')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.seconf.get')
    def test_chown_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, '/tmp/orphan_file'), (1, 'chown: failed'), (0, '')]

        # Mock test setup.
        S01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the owner and group of the files or directories without owner or group...")
        mock_logger.warning.assert_any_call("Set the owner and group of %s failed: %s", '/tmp/orphan_file', 'chown: failed')
        mock_logger.warning.assert_any_call("Set the owner and group of the files or directories failed")
        mock_Display.assert_called_once_with("- Set the owner and group of the files or directories...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.InsertSection')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.Display')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.logger')
    @patch('secScanner.enhance.euler.set.S01101_nouserfiles.seconf.get')
    def test_chown_partial_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：第一个 chown 成功，第二个 chown 失败，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, '/tmp/orphan_file\n/tmp/orphan_dir'), (0, ''), (1, ''), (0, '')]

        # Mock test setup.
        S01101_nouserfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the owner and group of the files or directories without owner or group...")
        self.assertEqual(mock_getstatusoutput.call_count, 4)
        mock_Display.assert_called_once_with("- Set the owner and group of the files or directories...", "FAILED")

if __name__ == '__main__':
    unittest.main()
