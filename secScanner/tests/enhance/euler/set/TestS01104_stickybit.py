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
import logging
from secScanner.enhance.euler.set.S01104_stickybit import S01104_stickybit  # Mock test setup.

class TestS01104_stickybit(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.Display')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.logger')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01104_stickybit()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_stickybit')
        mock_InsertSection.assert_called_once_with("Set the sticky bit on the world writable directories...")
        mock_getstatusoutput.assert_not_called()
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set the sticky bit on the world writable directories...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.Display')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.logger')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.seconf.get')
    def test_no_world_writable_dir_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：find 无输出，未执行 chmod，应视为 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the sticky bit on the world writable directories...")
        self.assertEqual(mock_getstatusoutput.call_count, 1)
        mock_run.assert_not_called()
        mock_logger.info.assert_called_once_with("No world writable directory without sticky bit found")
        mock_Display.assert_called_once_with("- No world writable directory without sticky bit found...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.Display')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.logger')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.seconf.get')
    def test_chmod_all_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/share_a\n/tmp/share_b')
        mock_run.return_value = MagicMock(returncode=0)

        # Mock test setup.
        S01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the sticky bit on the world writable directories...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['chmod', '+t', '/tmp/share_a'], capture_output=True)
        mock_run.assert_any_call(['chmod', '+t', '/tmp/share_b'], capture_output=True)
        mock_logger.info.assert_any_call("Set the sticky bit on %s finished", '/tmp/share_a')
        mock_Display.assert_called_once_with("- Set the sticky bit on the world writable directories...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.Display')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.logger')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.seconf.get')
    def test_chmod_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/share_a')
        mock_run.return_value = MagicMock(returncode=1)

        # Mock test setup.
        S01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the sticky bit on the world writable directories...")
        mock_logger.warning.assert_any_call("Set the sticky bit on %s failed", '/tmp/share_a')
        mock_logger.warning.assert_any_call("Set the sticky bit on the world writable directories failed")
        mock_Display.assert_called_once_with("- Set the sticky bit on the world writable directories...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.InsertSection')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.Display')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.logger')
    @patch('secScanner.enhance.euler.set.S01104_stickybit.seconf.get')
    def test_chmod_partial_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：第一个 chmod 成功，第二个失败，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/share_a\n/tmp/share_b')
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=1)]

        # Mock test setup.
        S01104_stickybit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Set the sticky bit on the world writable directories...")
        self.assertEqual(mock_run.call_count, 2)
        mock_Display.assert_called_once_with("- Set the sticky bit on the world writable directories...", "FAILED")

if __name__ == '__main__':
    unittest.main()
