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
from secScanner.enhance.euler.set.S01113_suidsgid import S01113_suidsgid  # Mock test setup.

class TestS01113_suidsgid(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.logger')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01113_suidsgid()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_suidsgid')
        mock_InsertSection.assert_called_once_with("Remove the unnecessary SUID and SGID bits of the files...")
        mock_getstatusoutput.assert_not_called()
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- Skip remove the unnecessary SUID and SGID bits of the files...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.logger')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.seconf.get')
    def test_remove_bits_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/usr/bin/su\n/usr/bin/foobar')
        mock_run.return_value = MagicMock(returncode=0)

        # Mock test setup.
        S01113_suidsgid()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the unnecessary SUID and SGID bits of the files...")
        mock_run.assert_called_once_with(['chmod', 'u-s,g-s', '/usr/bin/foobar'], capture_output=True)
        mock_logger.info.assert_any_call("The file %s is needed by the system, keep its SUID and SGID bits", '/usr/bin/su')
        mock_logger.info.assert_any_call("Remove the SUID and SGID bits of %s finished", '/usr/bin/foobar')
        mock_Display.assert_called_once_with("- Remove the unnecessary SUID and SGID bits of the files...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.logger')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.seconf.get')
    def test_chmod_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/usr/bin/foobar')
        mock_run.return_value = MagicMock(returncode=1)

        # Mock test setup.
        S01113_suidsgid()

        # Mock test setup.
        mock_run.assert_called_once_with(['chmod', 'u-s,g-s', '/usr/bin/foobar'], capture_output=True)
        mock_logger.warning.assert_any_call("Remove the SUID and SGID bits of %s failed", '/usr/bin/foobar')
        mock_logger.warning.assert_any_call("Remove the unnecessary SUID and SGID bits failed")
        mock_Display.assert_called_once_with("- Remove the unnecessary SUID and SGID bits of the files...", "FAILED")

    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.run')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.InsertSection')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.Display')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.logger')
    @patch('secScanner.enhance.euler.set.S01113_suidsgid.seconf.get')
    def test_only_whitelisted_files_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_run):
        """边界：find 结果全部为系统必需文件时，不执行 chmod 并判定 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (0, '/usr/bin/su\n/usr/bin/sudo')

        # Mock test setup.
        S01113_suidsgid()

        # Mock test setup.
        mock_run.assert_not_called()
        mock_Display.assert_called_once_with("- No file needs to remove the SUID and SGID bits...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
