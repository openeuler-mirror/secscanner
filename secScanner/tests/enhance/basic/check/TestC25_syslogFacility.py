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
from secScanner.enhance.basic.check.C25_syslogFacility import C25_syslogFacility

class TestC25_syslogFacility(unittest.TestCase):

    @patch('secScanner.enhance.basic.check.C25_syslogFacility.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="SyslogFacility AUTH\n")
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.logger')
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.Display')
    def test_syslog_facility_set_correctly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C25_syslogFacility()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has ssh syslogfacility set, checking ok")
        mock_display.assert_called_with("- Check the ssh syslogfacility...", "OK")

    @patch('secScanner.enhance.basic.check.C25_syslogFacility.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="SyslogFacility NOTAUTH\n")
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.logger')
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.Display')
    def test_syslog_facility_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C25_syslogFacility()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C25_02: %s", WRN_C25_02)
        mock_logger.warning.assert_any_call("SUG_C25: %s", SUG_C25)
        mock_display.assert_called_with("- Wrong ssh syslogfacility config set...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.logger')
    @patch('secScanner.enhance.basic.check.C25_syslogFacility.Display')
    def test_syslog_facility_not_set(self, mock_display, mock_logger, mock_file, mock_insert):
        # 运行测试的函数
        C25_syslogFacility()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C25_01: %s", WRN_C25_01)
        mock_logger.warning.assert_any_call("SUG_C25: %s", SUG_C25)
        mock_display.assert_called_with("- No ssh syslogfacility config set...", "WARNING")

if __name__ == '__main__':
    unittest.main()
