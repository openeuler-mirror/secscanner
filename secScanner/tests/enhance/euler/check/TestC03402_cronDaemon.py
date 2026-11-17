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
from unittest.mock import patch, mock_open, Mock
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03402_cronDaemon import C03402_cronDaemon  # Mock test setup.

class TestC03402_cronDaemon(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_cron_daemon_not_enabled_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = Mock(stdout=b'disabled')

        # Mock test setup.
        secScanner.enhance.euler.check.C03402_cronDaemon.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03402_cronDaemon()

        # Mock test setup.
        mock_run.assert_called_once_with(['systemctl', 'is-enabled', 'crond'], capture_output=True)
        mock_InsertSection.assert_called_once_with("Check whether the cron daemon is enabled")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03402\n")
        mock_logger.warning.assert_any_call("WRN_C03402: %s", WRN_C03402)
        mock_logger.warning.assert_any_call("SUG_C03402: %s", SUG_C03402)
        mock_Display.assert_called_once_with("- The cron daemon is not enabled...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_cron_daemon_enabled_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = Mock(stdout=b'enabled')

        # Mock test setup.
        C03402_cronDaemon()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the cron daemon is enabled")
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The cron daemon is enabled")
        mock_Display.assert_called_once_with("- Check whether the cron daemon is enabled...", "OK")

    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.check.C03402_cronDaemon.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_cron_daemon_output_with_whitespace_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：systemctl 输出带空白字符，strip 后为 enabled 应视为合规"""
        # Mock test setup.
        mock_run.return_value = Mock(stdout=b'  enabled \n')

        # Mock test setup.
        C03402_cronDaemon()

        # Mock test setup.
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The cron daemon is enabled")
        mock_Display.assert_called_once_with("- Check whether the cron daemon is enabled...", "OK")

if __name__ == '__main__':
    unittest.main()
