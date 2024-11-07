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
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C31_anonymousFTP import C31_anonymousFTP

class TestC31_anonymousFTP(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="anonymous_enable=NO\n")
    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.logger')
    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.Display')
    def test_anonymous_ftp_prohibited_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C31_anonymousFTP()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has prohibit anonymous FTP set, checking OK")
        mock_display.assert_called_with("- Check the prohibit anonymous FTP set...", "OK")


    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="anonymous_enable=YES\n")
    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.logger')
    @patch('secScanner.enhance.basic.check.C31_anonymousFTP.Display')
    def test_anonymous_ftp_allowed_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C31_anonymousFTP()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C31_02: %s", WRN_C31_02)
        mock_logger.warning.assert_any_call("SUG_C31: %s", SUG_C31)
        mock_display.assert_called_with("- Wrong prohibit anonymous FTP config set...", "WARNING")

if __name__ == '__main__':
    unittest.main()

