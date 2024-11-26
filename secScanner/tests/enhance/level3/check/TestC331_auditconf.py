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
from secScanner.enhance.level3.check.C331_auditconf import C331_auditconf

class TestC331_auditconf(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C331_auditconf.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="max_log_file_action = keep_logs\n")
    @patch('secScanner.enhance.level3.check.C331_auditconf.logger')
    @patch('secScanner.enhance.level3.check.C331_auditconf.Display')
    def test_audit_conf_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C331_auditconf()

        # 检查预期的日志信息是否已正确记录
        mock_logger.info.assert_called_with("audit.conf set correctly, checking ok")
        mock_display.assert_called_with("- Has set audit.conf correctly ...", "OK")

    @patch('secScanner.enhance.level3.check.C331_auditconf.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="max_log_file_action = rotate\n")
    @patch('secScanner.enhance.level3.check.C331_auditconf.logger')
    @patch('secScanner.enhance.level3.check.C331_auditconf.Display')
    def test_audit_conf_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        # 运行测试的函数
        C331_auditconf()

        # 检查预期的警告信息是否已正确记录
        mock_logger.warning.assert_any_call("WRN_C331: %s", WRN_C331)
        mock_logger.warning.assert_any_call("SUG_C331: %s", SUG_C331)
        mock_display.assert_called_with("- Wrong audit.conf set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C331_auditconf.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C331_auditconf.logger')
    @patch('secScanner.enhance.level3.check.C331_auditconf.Display')
    def test_config_file_does_not_exist(self, mock_display, mock_logger, mock_exists, mock_insert):
        # 运行测试的函数
        C331_auditconf()

        # 检查是否显示文件不存在的消息
        mock_logger.warning.assert_any_call(f"WRN_C331: /etc/audit/auditd.conf {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C331: /etc/audit/auditd.conf {SUG_no_file}")
        mock_display.assert_called_with("- Config file: /etc/audit/auditd.conf not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
