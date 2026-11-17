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
from unittest.mock import patch, mock_open
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C04206_journaldump import C04206_journaldump  # Mock test setup.

class TestC04206_journaldump(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04206_journaldump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.Display')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='*.info;mail.none\n')
    def test_journaldump_not_configured(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04206_journaldump.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04206_journaldump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check the rsyslog dump journald log config in /etc/rsyslog.conf")
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_any_call("\nC04206\n")
        mock_logger.warning.assert_any_call("WRN_C04206: %s", WRN_C04206)
        mock_logger.warning.assert_any_call("SUG_C04206: %s", SUG_C04206)
        mock_Display.assert_called_once_with("- The rsyslog dump journald log is not configured in /etc/rsyslog.conf...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04206_journaldump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.Display')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='module(load="imjournal")\n')
    def test_journaldump_configured(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04206_journaldump.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04206_journaldump()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check the rsyslog dump journald log config in /etc/rsyslog.conf")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_any_call("The rsyslog dump journald log is configured, checking OK")
        mock_Display.assert_called_once_with("- Check the rsyslog dump journald log config...", "OK")

    @patch('secScanner.enhance.euler.check.C04206_journaldump.os.path.exists')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.Display')
    @patch('secScanner.enhance.euler.check.C04206_journaldump.logger')
    @patch('builtins.open', new_callable=mock_open, read_data='#module(load="imjournal")\n\n')
    def test_journaldump_only_in_comment(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists):
        """边界：imjournal 仅出现在注释行中，应视为未配置"""
        # Mock test setup.
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C04206_journaldump.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04206_journaldump()

        # Mock test setup.
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_any_call("\nC04206\n")
        mock_Display.assert_called_once_with("- The rsyslog dump journald log is not configured in /etc/rsyslog.conf...", "WARNING")

if __name__ == '__main__':
    unittest.main()
