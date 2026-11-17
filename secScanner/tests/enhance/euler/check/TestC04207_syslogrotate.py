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
from unittest.mock import patch, mock_open, call
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C04207_syslogrotate import C04207_syslogrotate  # Mock test setup.

LOG_PATHS = ["/var/log/cron", "/var/log/maillog", "/var/log/messages", "/var/log/secure", "/var/log/spooler"]
FULL_CONFIG = '\n'.join(LOG_PATHS) + '\n{\n    maxage 365\n    rotate 30\n    compress\n    size +4096k\n}\n'

class TestC04207_syslogrotate(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='/var/log/cron\n')
    def test_rotate_not_configured(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04207_syslogrotate.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04207_syslogrotate()

        # Mock test setup.
        missing_paths = LOG_PATHS[1:]
        missing_params = ["maxage", "rotate", "compress", "size"]
        mock_InsertSection.assert_called_once_with("Check the rsyslog log rotate config in /etc/logrotate.d/rsyslog")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        self.assertEqual(mock_file().write.call_args_list.count(call("\nC04207\n")), 2)
        mock_logger.warning.assert_any_call("WRN_C04207_01: %s", WRN_C04207_01)
        mock_logger.warning.assert_any_call("SUG_C04207_01: %s", SUG_C04207_01)
        mock_logger.warning.assert_any_call("WRN_C04207_02: %s", WRN_C04207_02)
        mock_logger.warning.assert_any_call("SUG_C04207_02: %s", SUG_C04207_02)
        mock_Display.assert_any_call(f"- The rsyslog log rotate paths {missing_paths} are not configured...", "WARNING")
        mock_Display.assert_any_call(f"- The rsyslog log rotate params {missing_params} are not configured...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.logger')
    @patch('builtins.open', new_callable=mock_open, read_data=FULL_CONFIG)
    def test_rotate_configured(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04207_syslogrotate.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04207_syslogrotate()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check the rsyslog log rotate config in /etc/logrotate.d/rsyslog")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_any_call("The rsyslog log rotate paths are configured, checking OK")
        mock_logger.info.assert_any_call("The rsyslog log rotate params are configured, checking OK")
        mock_Display.assert_any_call("- Check the rsyslog log rotate paths config...", "OK")
        mock_Display.assert_any_call("- Check the rsyslog log rotate params config...", "OK")

    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.check.C04207_syslogrotate.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data='\n'.join(LOG_PATHS) + '\n{\n    notifempty\n    lastaction maxage 365\n}\n')
    def test_rotate_params_not_at_line_start(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：日志路径齐全，但 rotate 参数不出现在行首，应视为参数缺失"""
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04207_syslogrotate.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04207_syslogrotate()

        # Mock test setup.
        missing_params = ["maxage", "rotate", "compress", "size"]
        mock_Display.assert_any_call("- Check the rsyslog log rotate paths config...", "OK")
        mock_Display.assert_any_call(f"- The rsyslog log rotate params {missing_params} are not configured...", "WARNING")
        mock_file().write.assert_any_call("\nC04207\n")

if __name__ == '__main__':
    unittest.main()
