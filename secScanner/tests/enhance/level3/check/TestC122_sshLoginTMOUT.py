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
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C122_sshLoginTMOUT import C122_sshLoginTMOUT

class TestC122_sshLoginTMOUT(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="ClientAliveInterval 300\nClientAliveCountMax 0\n")
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.logger')
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.Display')
    def test_ssh_timeout_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C122_sshLoginTMOUT()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ssh login timeout set, checking OK")
        mock_display.assert_called_with("- Has ssh login timeout set...", "OK")

    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="ClientAliveInterval 1000\nClientAliveCountMax 3\n")
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.logger')
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.Display')
    def test_ssh_timeout_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C122_sshLoginTMOUT()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C122_01: %s", WRN_C122_01)
        mock_logger.warning.assert_any_call("SUG_C122_01: %s", SUG_C122_01)
        mock_display.assert_called_with("- Wrong ssh login timeout set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.logger')
    @patch('secScanner.enhance.level3.check.C122_sshLoginTMOUT.Display')
    def test_no_ssh_timeout_set(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C122_sshLoginTMOUT()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C122_02: %s", WRN_C122_02)
        mock_logger.warning.assert_any_call("SUG_C122_01: %s", SUG_C122_01)
        mock_display.assert_called_with("- No ssh login timeout set...", "WARNING")

if __name__ == '__main__':
    unittest.main()
