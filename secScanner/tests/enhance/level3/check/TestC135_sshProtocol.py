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
from secScanner.lib.function import InsertSection, Display
from secScanner.lib.textInfo_level3 import *
from secScanner.lib.textInfo_euler import WRN_no_file, SUG_no_file
from secScanner.enhance.level3.check.C135_sshProtocol import C135_sshProtocol

class TestC135_sshProtocol(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Protocol 2")
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.InsertSection')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.Display')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.logger')
    def test_ssh_protocol_correct(self, mock_logger, mock_display, mock_insert, mock_file, mock_exists):
        # 调用被测试函数
        C135_sshProtocol()

        # 验证函数行为
        mock_logger.info.assert_called_with("ssh Protocol set exists, checking ok")
        mock_display.assert_called_with("- check the ssh Protocol...", "OK")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="Protocol 1")
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.InsertSection')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.Display')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.logger')
    def test_ssh_protocol_incorrect(self, mock_logger, mock_display, mock_insert, mock_file, mock_exists):
        # 调用被测试函数
        C135_sshProtocol()

        # 验证函数行为
        mock_logger.warning.assert_any_call("WRN_C135_01: %s", WRN_C135_01)
        mock_logger.warning.assert_any_call("SUG_C135_01: %s", SUG_C135_01)
        mock_display.assert_called_with("- Set the ssh Protocol...", "WARNING")


    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.InsertSection')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.Display')
    @patch('secScanner.enhance.level3.check.C135_sshProtocol.logger')
    def test_ssh_protocol_not_set(self, mock_logger, mock_display, mock_insert, mock_file, mock_exists):
        # 调用被测试函数
        C135_sshProtocol()

        # 验证函数行为
        mock_logger.warning.assert_any_call("WRN_C135_01: %s", WRN_C135_01)
        mock_logger.warning.assert_any_call("SUG_C135_01: %s", SUG_C135_01)
        mock_display.assert_called_with("- Set the ssh Protocol...", "WARNING")

if __name__ == "__main__":
    unittest.main()
