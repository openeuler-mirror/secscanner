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
from secScanner.enhance.euler.set.S01103_hiddenexec import S01103_hiddenexec  # Mock test setup.

class TestS01103_hiddenexec(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.logger')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01103_hiddenexec()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_hiddenexec')
        mock_InsertSection.assert_called_once_with("Remove the executable permission of the hidden executable files...")
        mock_getstatusoutput.assert_not_called()
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip remove the executable permission of the hidden executable files...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.logger')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.seconf.get')
    def test_no_hidden_exec_file_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：find 无输出，未执行 chmod，应视为 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the executable permission of the hidden executable files...")
        self.assertEqual(mock_getstatusoutput.call_count, 1)
        mock_run.assert_not_called()
        mock_logger.info.assert_called_once_with("No hidden executable file found")
        mock_Display.assert_called_once_with("- No hidden executable file found...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.logger')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.seconf.get')
    def test_chmod_all_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/.hidden_a\n/tmp/.hidden_b')
        mock_run.return_value = MagicMock(returncode=0)

        # Mock test setup.
        S01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the executable permission of the hidden executable files...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['chmod', '644', '/tmp/.hidden_a'], capture_output=True)
        mock_run.assert_any_call(['chmod', '644', '/tmp/.hidden_b'], capture_output=True)
        mock_logger.info.assert_any_call("Remove the executable permission of %s finished", '/tmp/.hidden_a')
        mock_Display.assert_called_once_with("- Remove the executable permission of the hidden executable files...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.logger')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.seconf.get')
    def test_chmod_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/.hidden_a')
        mock_run.return_value = MagicMock(returncode=1)

        # Mock test setup.
        S01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the executable permission of the hidden executable files...")
        mock_logger.warning.assert_any_call("Remove the executable permission of %s failed", '/tmp/.hidden_a')
        mock_logger.warning.assert_any_call("Remove the executable permission of the hidden executable files failed")
        mock_Display.assert_called_once_with("- Remove the executable permission of the hidden executable files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.InsertSection')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.Display')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.logger')
    @patch('secScanner.enhance.euler.set.S01103_hiddenexec.seconf.get')
    def test_chmod_partial_failed_and_skip_except_files(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：except_files 被过滤，仅对剩余文件 chmod；其中一个失败应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/root/.bashrc\n/tmp/.hidden_a\n/tmp/.hidden_b')
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=1)]

        # Mock test setup.
        S01103_hiddenexec()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the executable permission of the hidden executable files...")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['chmod', '644', '/tmp/.hidden_a'], capture_output=True)
        mock_run.assert_any_call(['chmod', '644', '/tmp/.hidden_b'], capture_output=True)
        mock_Display.assert_called_once_with("- Remove the executable permission of the hidden executable files...", "FAILED")

if __name__ == '__main__':
    unittest.main()
