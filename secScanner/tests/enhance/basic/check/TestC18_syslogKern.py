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
from secScanner.enhance.basic.check.C18_syslogKern import C18_syslogKern

class TestC18_syslogKern(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C18_syslogKern.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="kern.warning /var/log/kern.log\n")
    @patch('secScanner.enhance.basic.check.C18_syslogKern.logger')
    @patch('secScanner.enhance.basic.check.C18_syslogKern.Display')
    def test_kern_warning_set_correctly(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        # 运行测试的函数
        C18_syslogKern()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("The security audit modle kern.warning is set, checking OK")
        mock_display.assert_called_with("- Check if there have kern.warning set...", "OK")

    @patch('secScanner.enhance.basic.check.C18_syslogKern.InsertSection')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', new_callable=mock_open, read_data="some unrelated config\n")
    @patch('secScanner.enhance.basic.check.C18_syslogKern.logger')
    @patch('secScanner.enhance.basic.check.C18_syslogKern.Display')
    def test_kern_warning_not_set(self, mock_display, mock_logger, mock_file, mock_getsize, mock_isfile, mock_insert):
        # 运行测试的函数
        C18_syslogKern()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C18: %s", WRN_C18)
        mock_display.assert_called_with("- Check if there have kern.warning set...", "WARNING")

if __name__ == '__main__':
    unittest.main()