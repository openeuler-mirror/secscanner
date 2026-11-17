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
from secScanner.enhance.euler.check.C01115_openfiles import C01115_openfiles  # Mock test setup.

class TestC01115_openfiles(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.Display')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_soft_limit_exceeds_hard_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, '4096'), (0, '1024')]
        mock_exists.return_value = True
        mock_file.return_value.readlines.return_value = []

        # Mock test setup.
        secScanner.enhance.euler.check.C01115_openfiles.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01115_openfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the open file limits of users are set correctly")
        mock_getstatusoutput.assert_any_call('ulimit -Sn')
        mock_getstatusoutput.assert_any_call('ulimit -Hn')
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01115\n")
        mock_logger.warning.assert_any_call("WRN_C01115_01: %s", WRN_C01115_01)
        mock_logger.warning.assert_any_call("SUG_C01115_01: %s", SUG_C01115_01)
        mock_Display.assert_any_call("- Check wrong set of the open file limits of the session...", "WARNING")
        mock_Display.assert_any_call("- Check the nofile limits in limits.conf...", "OK")

    @patch('secScanner.enhance.euler.check.C01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.Display')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="* soft nofile 4096\n* hard nofile 4096\n")
    def test_limits_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, '1024'), (0, '4096')]
        mock_exists.return_value = True

        # Mock test setup.
        C01115_openfiles()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the open file limits of users are set correctly")
        mock_logger.info.assert_any_call("The open file limits of the session are right, checking ok")
        mock_Display.assert_any_call("- Check the open file limits of the session...", "OK")
        mock_logger.info.assert_any_call("The nofile limits in limits.conf are right, checking ok")
        mock_Display.assert_any_call("- Check the nofile limits in limits.conf...", "OK")
        mock_file().write.assert_not_called()

    @patch('secScanner.enhance.euler.check.C01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.Display')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="* soft nofile 8192\n* hard nofile 4096\n")
    def test_limits_conf_soft_greater_than_hard_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_exists):
        """边界：会话限制正确，但 limits.conf 中 soft 大于 hard 应告警"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, '1024'), (0, '4096')]
        mock_exists.return_value = True

        # Mock test setup.
        secScanner.enhance.euler.check.C01115_openfiles.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01115_openfiles()

        # Mock test setup.
        mock_Display.assert_any_call("- Check the open file limits of the session...", "OK")
        mock_file().write.assert_called_once_with("\nC01115\n")
        mock_logger.warning.assert_any_call("WRN_C01115_02: %s", WRN_C01115_02)
        mock_logger.warning.assert_any_call("SUG_C01115_02: %s", SUG_C01115_02)
        mock_Display.assert_any_call("- Check wrong set of nofile limits in limits.conf...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01115_openfiles.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.InsertSection')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.Display')
    @patch('secScanner.enhance.euler.check.C01115_openfiles.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_ulimit_failed_and_config_missing_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_exists):
        """边界：ulimit 获取失败且 limits.conf 不存在，两处均应记录告警"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, ''), (1, '')]
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C01115_openfiles.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01115_openfiles()

        # Mock test setup.
        mock_Display.assert_any_call("- Failed to get the open file limits of the session...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C01115_01: %s", WRN_C01115_01)
        mock_logger.warning.assert_any_call("WRN_C01115_02: %s %s", '/etc/security/limits.conf', WRN_no_file)
        mock_Display.assert_any_call("- Config file: /etc/security/limits.conf not found...", "SKIPPING")
        self.assertEqual(mock_file().write.call_count, 2)
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")

if __name__ == '__main__':
    unittest.main()
