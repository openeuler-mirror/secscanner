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
from secScanner.enhance.level3.check.C421_nfsServer import C421_nfsServer

class TestC421_nfsServer(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.level3.check.C421_nfsServer.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'enabled'))
    @patch('secScanner.enhance.level3.check.C421_nfsServer.logger')
    @patch('secScanner.enhance.level3.check.C421_nfsServer.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_nfs_server_enabled(self, mock_open, mock_display, mock_logger, mock_subproc, mock_insert):
        # 运行测试的函数
        C421_nfsServer()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C421: %s", WRN_C421)
        mock_logger.warning.assert_any_call("SUG_C421: %s", SUG_C421)
        mock_display.assert_called_with("- Check the nfs-Server is enabled...", "WARNING")

    @patch('secScanner.enhance.level3.check.C421_nfsServer.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C421_nfsServer.logger')
    @patch('secScanner.enhance.level3.check.C421_nfsServer.Display')
    def test_nfs_server_disabled(self, mock_display, mock_logger, mock_subproc, mock_insert):
        # 运行测试的函数
        C421_nfsServer()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("The nfs-Server status is: disabled")
        mock_display.assert_called_with("- Check the nfs-Server is disabled...", "OK")

if __name__ == '__main__':
    unittest.main()
