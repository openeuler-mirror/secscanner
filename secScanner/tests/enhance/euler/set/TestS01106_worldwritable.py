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
from secScanner.enhance.euler.set.S01106_worldwritable import S01106_worldwritable  # Mock test setup.

class TestS01106_worldwritable(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.InsertSection')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.Display')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.logger')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01106_worldwritable()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_worldwritable')
        mock_InsertSection.assert_called_once_with("Remove the world writable permission of the files...")
        mock_getstatusoutput.assert_not_called()
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip remove the world writable permission of the files...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.InsertSection')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.Display')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.logger')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.seconf.get')
    def test_no_world_writable_file_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：find 无输出，未执行 chmod，应视为 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S01106_worldwritable()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the world writable permission of the files...")
        self.assertEqual(mock_getstatusoutput.call_count, 1)
        mock_run.assert_not_called()
        mock_logger.info.assert_called_once_with("No world writable file found")
        mock_Display.assert_called_once_with("- No world writable file found...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.InsertSection')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.Display')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.logger')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.seconf.get')
    def test_chmod_all_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/writable_a\n/tmp/writable_b')
        mock_run.return_value = MagicMock(returncode=0)

        # Mock test setup.
        S01106_worldwritable()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the world writable permission of the files...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['chmod', 'o-w', '/tmp/writable_a'], capture_output=True)
        mock_run.assert_any_call(['chmod', 'o-w', '/tmp/writable_b'], capture_output=True)
        mock_logger.info.assert_any_call("Remove the world writable permission of %s finished", '/tmp/writable_a')
        mock_Display.assert_called_once_with("- Remove the world writable permission of the files...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.InsertSection')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.Display')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.logger')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.seconf.get')
    def test_chmod_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/writable_a')
        mock_run.return_value = MagicMock(returncode=1)

        # Mock test setup.
        S01106_worldwritable()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the world writable permission of the files...")
        mock_logger.warning.assert_any_call("Remove the world writable permission of %s failed", '/tmp/writable_a')
        mock_logger.warning.assert_any_call("Remove the world writable permission of the files failed")
        mock_Display.assert_called_once_with("- Remove the world writable permission of the files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.InsertSection')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.Display')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.logger')
    @patch('secScanner.enhance.euler.set.S01106_worldwritable.seconf.get')
    def test_chmod_partial_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：第一个 chmod 成功，第二个失败，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/writable_a\n/tmp/writable_b')
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=1)]

        # Mock test setup.
        S01106_worldwritable()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the world writable permission of the files...")
        self.assertEqual(mock_run.call_count, 2)
        mock_Display.assert_called_once_with("- Remove the world writable permission of the files...", "FAILED")

if __name__ == '__main__':
    unittest.main()
