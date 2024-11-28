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
from secScanner.enhance.level3.check.C332_auditconf2 import C332_auditconf2

class TestC332_auditconf2(unittest.TestCase):

    @patch('secScanner.enhance.level3.check.C332_auditconf2.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="space_left_action = email\naction_mail_acct = root\nadmin_space_left_action = halt\n")
    @patch('secScanner.enhance.level3.check.C332_auditconf2.logger')
    @patch('secScanner.enhance.level3.check.C332_auditconf2.Display')
    def test_audit_conf_set_correctly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        C332_auditconf2()
        mock_logger.info.assert_called_with("audit.conf set correctly, checking ok")
        mock_display.assert_called_with("- Has set audit.conf correctly ...", "OK")

    @patch('secScanner.enhance.level3.check.C332_auditconf2.InsertSection')
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="space_left_action = syslog\naction_mail_acct = admin\nadmin_space_left_action = suspend\n")
    @patch('secScanner.enhance.level3.check.C332_auditconf2.logger')
    @patch('secScanner.enhance.level3.check.C332_auditconf2.Display')
    def test_audit_conf_set_incorrectly(self, mock_display, mock_logger, mock_file, mock_exists, mock_insert):
        C332_auditconf2()
        mock_logger.warning.assert_any_call("WRN_C332: %s", WRN_C332)
        mock_logger.warning.assert_any_call("SUG_C332: %s", SUG_C332)
        mock_display.assert_called_with("- Wrong audit.conf set...", "WARNING")

    @patch('secScanner.enhance.level3.check.C332_auditconf2.InsertSection')
    @patch('os.path.exists', return_value=False)
    @patch('secScanner.enhance.level3.check.C332_auditconf2.logger')
    @patch('secScanner.enhance.level3.check.C332_auditconf2.Display')
    def test_config_file_does_not_exist(self, mock_display, mock_logger, mock_exists, mock_insert):
        C332_auditconf2()
        mock_logger.warning.assert_any_call(f"WRN_C332: /etc/audit/auditd.conf {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C332: /etc/audit/auditd.conf {SUG_no_file}")
        mock_display.assert_called_with("- Config file: /etc/audit/auditd.conf not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
