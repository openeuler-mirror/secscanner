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
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C12_sshGssapi import C12_sshGssapi

# 定义测试类
class TestC12_sshGssapi(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C12_sshGssapi.Display')
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="GSSAPIAuthentication no\n")
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.logger')
    def test_gssapi_config_set_no(self, mock_logger, mock_file, mock_insert, mock_display):
        # 运行测试的函数
        C12_sshGssapi()

        # 检查预期的日志信息是否已正确记录
        mock_logger.warning.assert_called_with("Has ssh gssapi set, checking ok")

    @patch('secScanner.enhance.basic.check.C12_sshGssapi.Display')
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="GSSAPIAuthentication yes\n")
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.logger')
    def test_gssapi_config_set_incorrect(self, mock_logger, mock_file, mock_insert, mock_display):
        # 运行测试的函数
        C12_sshGssapi()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C12_01: %s", WRN_C12_01)
        mock_logger.warning.assert_any_call("SUG_C12: %s", SUG_C12)
    
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.Display')
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C12_sshGssapi.logger')
    def test_no_gssapi_config(self, mock_logger, mock_file, mock_insert, mock_display):
        # 运行测试的函数
        C12_sshGssapi()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C12_02: %s", WRN_C12_02)
        mock_logger.warning.assert_any_call("SUG_C12: %s", SUG_C12)


if __name__ == '__main__':
    unittest.main()

