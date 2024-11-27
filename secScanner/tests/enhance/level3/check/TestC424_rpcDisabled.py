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
from secScanner.enhance.level3.check.C424_rpcDisabled import C424_rpcDisabled

class TestC424_rpcDisabled(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.logger')
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.Display')
    def test_rpc_service_disabled(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C424_rpcDisabled()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has right rpcbind service set, checking ok")
        mock_display.assert_called_with("- Has right rpcbind service set: disabled...", "OK")

    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'masked'))
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.logger')
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.Display')
    def test_rpc_service_masked(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C424_rpcDisabled()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has right rpcbind service set, checking ok")
        mock_display.assert_called_with("- Has right rpcbind service set: masked...", "OK")

    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'Failed to get unit file state'))
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.logger')
    @patch('secScanner.enhance.level3.check.C424_rpcDisabled.Display')
    def test_rpc_service_not_exist(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C424_rpcDisabled()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("No rpcbind service, checking ok")
        mock_display.assert_called_with("- No rpcbind service, checking ok...", "OK")

if __name__ == '__main__':
    unittest.main()
