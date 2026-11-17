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
from unittest.mock import patch, mock_open
import logging
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C04101_auditd import C04101_auditd  # Mock test setup.

class TestC04101_auditd(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04101_auditd.Display')
    @patch('secScanner.enhance.euler.check.C04101_auditd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_not_installed(self, mock_file, mock_logger, mock_Display,
                                 mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(1, 'package audit is not installed'),
                                            (1, 'package audit-libs is not installed')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04101_auditd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04101_auditd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check the auditd service status in your Linux System")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04101\n")
        mock_logger.warning.assert_any_call("WRN_C04101_01: %s", WRN_C04101_01)
        mock_logger.warning.assert_any_call("SUG_C04101_01: %s", SUG_C04101_01)
        mock_Display.assert_called_once_with("- The audit or audit-libs software is not installed...", "WARNING")

    @patch('secScanner.enhance.euler.check.C04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04101_auditd.Display')
    @patch('secScanner.enhance.euler.check.C04101_auditd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_audit_installed_enabled_active(self, mock_file, mock_logger, mock_Display,
                                            mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'audit-3.0.7'),
                                            (0, 'audit-libs-3.0.7'),
                                            (0, 'enabled'),
                                            (0, 'active')]

        # Mock test setup.
        C04101_auditd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check the auditd service status in your Linux System")
        mock_Display.assert_any_call("- Check the audit and audit-libs software is installed...", "OK")
        mock_Display.assert_any_call("- Check the auditd service is enabled...", "OK")
        mock_Display.assert_any_call("- Check the auditd service is active...", "OK")
        mock_file.assert_not_called()

    @patch('secScanner.enhance.euler.check.C04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04101_auditd.Display')
    @patch('secScanner.enhance.euler.check.C04101_auditd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_auditd_not_enabled(self, mock_file, mock_logger, mock_Display,
                                mock_InsertSection, mock_getstatusoutput):
        """边界：软件已安装且服务 active，但 is-enabled 返回非 0，应 WARNING"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'audit-3.0.7'),
                                            (0, 'audit-libs-3.0.7'),
                                            (1, 'disabled'),
                                            (0, 'active')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04101_auditd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04101_auditd()

        # Mock test setup.
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC04101\n")
        mock_logger.warning.assert_any_call("WRN_C04101_02: %s", WRN_C04101_02)
        mock_logger.warning.assert_any_call("SUG_C04101_02: %s", SUG_C04101_02)
        mock_Display.assert_any_call("- Check the audit and audit-libs software is installed...", "OK")
        mock_Display.assert_any_call("- Check the status of auditd is disabled...", "WARNING")
        mock_Display.assert_any_call("- Check the auditd service is active...", "OK")

    @patch('secScanner.enhance.euler.check.C04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.check.C04101_auditd.Display')
    @patch('secScanner.enhance.euler.check.C04101_auditd.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_auditd_not_active(self, mock_file, mock_logger, mock_Display,
                               mock_InsertSection, mock_getstatusoutput):
        """边界：服务 enabled 但返回 inactive，应 WARNING 并标记 C04101"""
        # Mock test setup.
        mock_getstatusoutput.side_effect = [(0, 'audit-3.0.7'),
                                            (0, 'audit-libs-3.0.7'),
                                            (0, 'enabled'),
                                            (0, 'inactive')]

        # Mock test setup.
        secScanner.enhance.euler.check.C04101_auditd.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C04101_auditd()

        # Mock test setup.
        mock_file().write.assert_called_once_with("\nC04101\n")
        mock_logger.warning.assert_any_call("WRN_C04101_03: %s", WRN_C04101_03)
        mock_logger.warning.assert_any_call("SUG_C04101_03: %s", SUG_C04101_03)
        mock_Display.assert_any_call("- Check the auditd service is enabled...", "OK")
        mock_Display.assert_any_call("- Check the status of auditd is inactive...", "WARNING")

if __name__ == '__main__':
    unittest.main()
