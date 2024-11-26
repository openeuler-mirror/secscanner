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
from secScanner.lib import *
from secScanner.enhance.level3.check.C311_auditEnabled import C311_auditEnabled

class TestC311_auditEnabled(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C311_auditEnabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'enabled'))
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.logger')
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.Display')
    def test_audit_service_enabled(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C311_auditEnabled()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Has right auditd service set, checking ok")
        mock_display.assert_called_with("- Has right auditd service set: enabled...", "OK")

    @patch('secScanner.enhance.level3.check.C311_auditEnabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'disabled'))
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.logger')
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_service_disabled(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C311_auditEnabled()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C311: %s", WRN_C311_01)
        mock_logger.warning.assert_any_call("SUG_C311: %s", SUG_C311_01)
        mock_display.assert_called_with("- Wrong auditd service status...", "WARNING")

    @patch('secScanner.enhance.level3.check.C311_auditEnabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(1, 'Failed to get unit file state'))
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.logger')
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.Display')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_service_not_installed(self, mock_file, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C311_auditEnabled()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C311: %s", WRN_C311_02)
        mock_logger.warning.assert_any_call("SUG_C311: %s", SUG_C311_02)
        mock_display.assert_called_with("- No auditd service, need to install...", "WARNING")

    @patch('secScanner.enhance.level3.check.C311_auditEnabled.InsertSection')
    @patch('subprocess.getstatusoutput', return_value=(0, 'unknown'))
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.logger')
    @patch('secScanner.enhance.level3.check.C311_auditEnabled.Display')
    def test_audit_service_unexpected_status(self, mock_display, mock_logger, mock_subprocess, mock_insert):
        # 运行测试的函数
        C311_auditEnabled()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("Unexpected status of auditd")
        mock_display.assert_called_with("- Unexpected status of auditd...", "WARNING")

if __name__ == '__main__':
    unittest.main()