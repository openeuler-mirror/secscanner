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
from unittest.mock import patch, mock_open, MagicMock
import logging
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03517_timewait import C03517_timewait

class TestC03517_timewait(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03517_timewait.RESULT_FILE', 'check_result.relt')
    @patch('secScanner.enhance.euler.check.C03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.check.C03517_timewait.Display')
    @patch('secScanner.enhance.euler.check.C03517_timewait.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_fin_timeout_greater_than_60_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 120\n")

        # Mock test setup.
        C03517_timewait()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the TIME WAIT tcp fin timeout is right set")
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.tcp_fin_timeout'], capture_output=True)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03517\n")
        mock_logger.warning.assert_any_call("WRN_C03517: %s", WRN_C03517)
        mock_logger.warning.assert_any_call("SUG_C03517: %s", SUG_C03517)
        mock_Display.assert_called_once_with("- The TIME WAIT tcp fin timeout is greater than 60...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.check.C03517_timewait.Display')
    @patch('secScanner.enhance.euler.check.C03517_timewait.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_fin_timeout_less_than_60_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        # Mock test setup.
        mock_run.return_value = MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 30\n")

        # Mock test setup.
        C03517_timewait()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the TIME WAIT tcp fin timeout is right set")
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The TIME WAIT tcp fin timeout is right set")
        mock_Display.assert_called_once_with("- Check whether the TIME WAIT tcp fin timeout is right set...", "OK")

    @patch('secScanner.enhance.euler.check.C03517_timewait.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03517_timewait.InsertSection')
    @patch('secScanner.enhance.euler.check.C03517_timewait.Display')
    @patch('secScanner.enhance.euler.check.C03517_timewait.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_fin_timeout_equal_60_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：tcp_fin_timeout 恰好等于 60（不大于 60）应判为合规"""
        # Mock test setup.
        mock_run.return_value = MagicMock(stdout=b"net.ipv4.tcp_fin_timeout = 60\n")

        # Mock test setup.
        C03517_timewait()

        # Mock test setup.
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the TIME WAIT tcp fin timeout is right set...", "OK")

if __name__ == '__main__':
    unittest.main()
