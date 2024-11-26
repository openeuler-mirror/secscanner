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
from secScanner.enhance.level3.check.C257_groupxProperty import C257_groupxProperty

class TestC257_groupxProperty(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C257_groupxProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw-r--r-- 1 root root 123456 Jul 10 10:00 /etc/group-"))
    @patch('secScanner.enhance.level3.check.C257_groupxProperty.logger')
    @patch('secScanner.enhance.level3.check.C257_groupxProperty.Display')
    def test_groupx_permissions_correct(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C257_groupxProperty()

        # 验证权限正确时的操作
        mock_display.assert_called_with("- check if /etc/group- property is 644 ...", "OK")

    @patch('secScanner.enhance.level3.check.C257_groupxProperty.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('subprocess.getstatusoutput', return_value=(0, "-rw------- 1 root root 123456 Jul 10 10:00 /etc/group-"))
    @patch('secScanner.enhance.level3.check.C257_groupxProperty.logger')
    @patch('secScanner.enhance.level3.check.C257_groupxProperty.Display')
    def test_groupx_permissions_incorrect(self, mock_display, mock_logger, mock_subprocess, mock_exists, mock_insert):
        # 运行测试的函数
        C257_groupxProperty()

        # 验证权限不正确时的操作
        mock_logger.warning.assert_any_call("WRN_C257: %s", WRN_C257)
        mock_logger.warning.assert_any_call("SUG_C257: %s", SUG_C257)
        mock_display.assert_called_with("- Check if /etc/group- property is not 644...", "WARNING")

    @patch('secScanner.enhance.level3.check.C257_groupxProperty.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C257_groupxProperty.Display')
    def test_groupx_file_not_exist(self, mock_display, mock_exists, mock_insert):
        # 运行测试的函数
        C257_groupxProperty()

        # 验证文件不存在时的操作
        mock_display.assert_called_with("- file '/etc/group-' does not exist...", "SKIPPED")

if __name__ == '__main__':
    unittest.main()
