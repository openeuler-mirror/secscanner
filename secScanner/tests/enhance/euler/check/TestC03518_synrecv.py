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
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03518_synrecv import C03518_synrecv

class TestC03518_synrecv(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.Display')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_backlog_less_than_256_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """不合规：队列长度 128 小于 256，应告警并写入 RESULT_FILE"""
        mock_run.return_value = Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 128")

        secScanner.enhance.euler.check.C03518_synrecv.RESULT_FILE = "check_result.relt"

        C03518_synrecv()

        mock_InsertSection.assert_called_once_with("Check whether the SYN_RECV state queue number is right set")
        mock_run.assert_called_once_with(['sysctl', 'net.ipv4.tcp_max_syn_backlog'], capture_output=True)
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03518\n")
        mock_logger.warning.assert_any_call("WRN_C03518: %s", WRN_C03518)
        mock_logger.warning.assert_any_call("SUG_C03518: %s", SUG_C03518)
        mock_Display.assert_called_once_with("- The SYN_RECV state queue number is less than 256...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.Display')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_backlog_greater_than_256_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """合规：队列长度 1024 不小于 256，不写 RESULT_FILE"""
        mock_run.return_value = Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 1024")

        C03518_synrecv()

        mock_InsertSection.assert_called_once_with("Check whether the SYN_RECV state queue number is right set")
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The SYN_RECV state queue number is right set")
        mock_Display.assert_called_once_with("- Check whether the SYN_RECV state queue number is right set...", "OK")

    @patch('secScanner.enhance.euler.check.C03518_synrecv.subprocess.run')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.InsertSection')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.Display')
    @patch('secScanner.enhance.euler.check.C03518_synrecv.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_backlog_exactly_256_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_run):
        """边界：队列长度恰好 256（带尾随空白与换行），应判定合规"""
        mock_run.return_value = Mock(stdout=b"net.ipv4.tcp_max_syn_backlog = 256\n")

        C03518_synrecv()

        mock_file.assert_not_called()
        mock_logger.warning.assert_not_called()
        mock_Display.assert_called_once_with("- Check whether the SYN_RECV state queue number is right set...", "OK")

if __name__ == '__main__':
    unittest.main()
