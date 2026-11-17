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
from secScanner.enhance.euler.set.S01102_nulllink import S01102_nulllink  # Mock test setup.

class TestS01102_nulllink(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.Display')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.logger')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01102_nulllink()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_nulllink')
        mock_InsertSection.assert_called_once_with("Remove the null link files...")
        mock_Display.assert_called_once_with("- Skip remove the null link files...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.Display')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.logger')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.seconf.get')
    def test_remove_all_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/broken_link1\n/tmp/broken_link2')
        mock_run.return_value.returncode = 0

        # Mock test setup.
        S01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the null link files...")
        mock_getstatusoutput.assert_called_once_with("find / -xdev -type l -follow 2>/dev/null")
        self.assertEqual(mock_run.call_count, 2)
        mock_run.assert_any_call(['rm', '-f', '/tmp/broken_link1'], capture_output=True)
        mock_run.assert_any_call(['rm', '-f', '/tmp/broken_link2'], capture_output=True)
        mock_Display.assert_called_once_with("- Remove the null link files...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.Display')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.logger')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.seconf.get')
    def test_remove_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/broken_link')
        mock_run.return_value.returncode = 1

        # Mock test setup.
        S01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the null link files...")
        mock_run.assert_called_once_with(['rm', '-f', '/tmp/broken_link'], capture_output=True)
        mock_logger.warning.assert_any_call("Remove the null link file %s failed", '/tmp/broken_link')
        mock_logger.warning.assert_any_call("Remove the null link files failed")
        mock_Display.assert_called_once_with("- Remove the null link files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.Display')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.logger')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.seconf.get')
    def test_remove_partial_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_getstatusoutput):
        """边界：第一个 rm 成功，第二个 rm 失败，应视为 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/tmp/broken_link1\n/tmp/broken_link2')
        mock_run.side_effect = [self._make_result(0), self._make_result(1)]

        # Mock test setup.
        S01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the null link files...")
        self.assertEqual(mock_run.call_count, 2)
        mock_Display.assert_called_once_with("- Remove the null link files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.InsertSection')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.Display')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.logger')
    @patch('secScanner.enhance.euler.set.S01102_nulllink.seconf.get')
    def test_no_nulllink_found_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_run, mock_getstatusoutput):
        """边界：find 无结果时应提示 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S01102_nulllink()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the null link files...")
        mock_logger.info.assert_called_once_with("No null link file found")
        mock_Display.assert_called_once_with("- No null link file found...", "SKIPPING")

    @staticmethod
    def _make_result(returncode):
        """构造 mock 的 subprocess.run 返回结果"""
        result = unittest.mock.Mock()
        result.returncode = returncode
        return result

if __name__ == '__main__':
    unittest.main()
