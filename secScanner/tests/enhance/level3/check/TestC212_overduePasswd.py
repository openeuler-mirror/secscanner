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
import time
from secScanner.lib.textInfo_level3 import *
from secScanner.enhance.level3.check.C212_overduePasswd import C212_overduePasswd

class TestC212_overduePasswd(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C212_overduePasswd.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('time.time', return_value=1700000000)  # 固定当前时间戳
    @patch('builtins.open', new_callable=mock_open, read_data="root:$6$xyz:19650:0:99999:7:::\nuser1:$6$abc:19650:0:99999:7:::\n")
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.logger')
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.Display')
    @patch('builtins.print')
    def test_no_expired_passwords(self, mock_print, mock_display, mock_logger, mock_file, mock_time, mock_exists, mock_insert):
        # 运行测试的函数
        C212_overduePasswd()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with('No expired password exists, checking ok')
        mock_display.assert_called_with("- No expired password exists", "OK")

    @patch('secScanner.enhance.level3.check.C212_overduePasswd.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('time.time', return_value=1700000000)  # 固定当前时间戳
    @patch('builtins.open', new_callable=mock_open, read_data="root:$6$xyz:17000:0:30:7:::\nuser1:$6$abc:17000:0:30:7:::\n")
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.logger')
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.Display')
    @patch('builtins.print')
    def test_expired_passwords_exist(self, mock_print, mock_display, mock_logger, mock_file, mock_time, mock_exists, mock_insert):
        # 运行测试的函数
        C212_overduePasswd()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C212_01: %s", WRN_C212_01)
        mock_logger.warning.assert_any_call("SUG_C212_01: %s", SUG_C212_01)
        mock_display.assert_called_with("- At least one password has expired", "WARNING")

    @patch('secScanner.enhance.level3.check.C212_overduePasswd.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.logger')
    @patch('secScanner.enhance.level3.check.C212_overduePasswd.Display')
    def test_shadow_file_not_exist(self, mock_display, mock_logger, mock_exists, mock_insert):
        # 运行测试的函数
        C212_overduePasswd()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C212_02: %s", WRN_C212_02)
        mock_logger.warning.assert_any_call("SUG_C212_02: %s", SUG_C212_02)
        mock_display.assert_called_with("- file /etc/shadow dose not exist...", "WARNING")

if __name__ == '__main__':
    unittest.main()
