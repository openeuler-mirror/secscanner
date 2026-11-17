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
from unittest.mock import patch
import logging
from secScanner.enhance.euler.set.S04101_auditd import S04101_auditd  # Mock test setup.

class TestS04101_auditd(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04101_auditd.Display')
    @patch('secScanner.enhance.euler.set.S04101_auditd.logger')
    @patch('secScanner.enhance.euler.set.S04101_auditd.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04101_auditd()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_auditd')
        mock_InsertSection.assert_called_once_with("Enable and start the auditd service in your Linux System...")
        mock_Display.assert_called_once_with("- Skip set enable the auditd due to config file...", "SKIPPING")
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04101_auditd.Display')
    @patch('secScanner.enhance.euler.set.S04101_auditd.logger')
    @patch('secScanner.enhance.euler.set.S04101_auditd.seconf.get')
    def test_already_enabled_and_active_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                                 mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'audit-3.0.7'),
                                            (0, 'enabled'),
                                            (0, 'active')]

        # Mock test setup.
        S04101_auditd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Enable and start the auditd service in your Linux System...")
        self.assertEqual(mock_getstatusoutput.call_count, 3)
        mock_logger.info.assert_any_call('The auditd is already enabled and active')
        mock_Display.assert_called_once_with("- The auditd is already enabled and active...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04101_auditd.Display')
    @patch('secScanner.enhance.euler.set.S04101_auditd.logger')
    @patch('secScanner.enhance.euler.set.S04101_auditd.seconf.get')
    def test_install_and_start_finished(self, mock_seconf_get, mock_logger, mock_Display,
                                        mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(1, 'package audit is not installed'),
                                            (0, 'installed'),
                                            (1, 'disabled'),
                                            (1, 'inactive'),
                                            (0, ''),
                                            (0, '')]

        # Mock test setup.
        S04101_auditd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Enable and start the auditd service in your Linux System...")
        mock_getstatusoutput.assert_any_call('rpm -q audit')
        mock_getstatusoutput.assert_any_call('dnf install -y audit audit-libs')
        mock_getstatusoutput.assert_any_call('systemctl enable auditd.service')
        mock_getstatusoutput.assert_any_call('systemctl start auditd.service')
        mock_Display.assert_any_call("- Install the audit and audit-libs software...", "FINISHED")
        mock_Display.assert_any_call("- Set enable and start the auditd...", "FINISHED")
        self.assertEqual(mock_getstatusoutput.call_count, 6)

    @patch('secScanner.enhance.euler.set.S04101_auditd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04101_auditd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04101_auditd.Display')
    @patch('secScanner.enhance.euler.set.S04101_auditd.logger')
    @patch('secScanner.enhance.euler.set.S04101_auditd.seconf.get')
    def test_enable_failed(self, mock_seconf_get, mock_logger, mock_Display,
                           mock_InsertSection, mock_getstatusoutput):
        """边界：软件已安装但 enable 失败，应 FAILED 并提前返回"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'audit-3.0.7'),
                                            (1, 'disabled'),
                                            (1, 'inactive'),
                                            (1, 'Failed to enable unit')]

        # Mock test setup.
        S04101_auditd()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Enable and start the auditd service in your Linux System...")
        mock_logger.error.assert_called_once_with('Failed to enable the auditd :Failed to enable unit')
        mock_Display.assert_called_once_with("- Set enable the auditd...", "FAILED")
        self.assertEqual(mock_getstatusoutput.call_count, 4)
        mock_getstatusoutput.assert_any_call('systemctl enable auditd.service')

if __name__ == '__main__':
    unittest.main()
