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
from secScanner.enhance.basic.check.C15_disableUnUsedSoft import C15_disableUnUsedSoft, softck

class TestC15_disableUnUsedSoft(unittest.TestCase):
    def setUp(self):
        # 设置日志记录器
        self.logger = MagicMock()

    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.InsertSection')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.get_value', side_effect=['openeuler', '7'])
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.seconf.get', return_value='httpd.service nginx.service')
    @patch('subprocess.getstatusoutput', return_value=(0, 'httpd.service loaded active\nnginx.service loaded active\n'))
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.logger')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.Display')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.open')
    def test_unwanted_services_running(self, mock_open, mock_display, mock_logger, mock_subproc, mock_config, mock_get_value, mock_insert):
        # 运行测试的函数
        C15_disableUnUsedSoft()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C15_01: %s", WRN_C15_01)
        mock_display.assert_called_with("- Service httpd.service nginx.service  need stop...", "WARNING")

    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.InsertSection')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.get_value', side_effect=['openeuler', '7'])
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.seconf.get', return_value='httpd.service nginx.service')
    @patch('subprocess.getstatusoutput', return_value=(0, ''))
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.logger')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.Display')
    def test_no_services_running(self, mock_display, mock_logger, mock_subproc, mock_config, mock_get_value, mock_insert):
        # 运行测试的函数
        C15_disableUnUsedSoft()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C15_02: %s", WRN_C15_02)
        mock_display.assert_called_with("- No service need stop...", "OK")
    
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.InsertSection')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.get_value', side_effect=['unknown', 'unknown'])
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.logger')
    @patch('secScanner.enhance.basic.check.C15_disableUnUsedSoft.Display')
    def test_unsupported_os(self, mock_display, mock_logger, mock_get_value, mock_insert):
        # 运行测试的函数
        C15_disableUnUsedSoft()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_called_with(f"C15: This is unknown os-distro, we do not support unknown-unknown at this moment")
        mock_display.assert_called_with("- We do not support unknown-unknown at this moment...", "WARNING")

if __name__ == '__main__':
    unittest.main()