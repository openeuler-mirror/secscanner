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
from secScanner.enhance.euler.set.S04201_rsyslogd import S04201_rsyslogd  # Mock test setup.

SECTION = "Enable and start the rsyslog service in your Linux System..."

class TestS04201_rsyslogd(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_rsyslogd')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("- Skip set enable the rsyslog due to config file...", "SKIPPING")
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_enable_and_start_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'disabled'),
                                           (3, 'inactive'),
                                           (0, ''),
                                           (0, '')]

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_rsyslogd')
        mock_InsertSection.assert_called_once_with(SECTION)
        self.assertEqual(mock_getstatusoutput.call_count, 5)
        mock_getstatusoutput.assert_any_call('systemctl enable rsyslog.service')
        mock_getstatusoutput.assert_any_call('systemctl start rsyslog.service')
        mock_Display.assert_called_once_with("- Set enable and start the rsyslog...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_already_enabled_and_active_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：已安装且已 enable、已 active，不应再执行 enable/start，应 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (0, 'enabled'),
                                           (0, 'active')]

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        self.assertEqual(mock_getstatusoutput.call_count, 3)
        mock_Display.assert_called_once_with("- The rsyslog is already enabled and active...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_enable_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'disabled'),
                                           (3, 'inactive'),
                                           (1, 'enable failed')]

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        mock_logger.error.assert_called_once_with('Failed to enable the rsyslog :enable failed')
        mock_Display.assert_called_once_with("- Set enable the rsyslog...", "FAILED")
        self.assertEqual(mock_getstatusoutput.call_count, 4)

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_start_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'rsyslog-8.2102.0-11.oe2203'),
                                           (1, 'disabled'),
                                           (3, 'inactive'),
                                           (0, ''),
                                           (1, 'start failed')]

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        mock_logger.error.assert_called_once_with('Failed to start the rsyslog :start failed')
        mock_Display.assert_called_once_with("- Set start the rsyslog...", "FAILED")

    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.InsertSection')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.Display')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.logger')
    @patch('secScanner.enhance.euler.set.S04201_rsyslogd.seconf.get')
    def test_install_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：未安装且 dnf、yum 均安装失败，应 FAILED 且不再继续 enable/start"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(1, 'package rsyslog is not installed'),
                                           (1, 'dnf failed'),
                                           (1, 'yum failed')]

        # Mock test setup.
        S04201_rsyslogd()

        # Mock test setup.
        self.assertEqual(mock_getstatusoutput.call_count, 3)
        mock_getstatusoutput.assert_any_call('dnf install -y rsyslog')
        mock_getstatusoutput.assert_any_call('yum install -y rsyslog')
        mock_logger.error.assert_called_once_with('Failed to install the rsyslog software :yum failed')
        mock_Display.assert_called_once_with("- Install the rsyslog software...", "FAILED")

if __name__ == '__main__':
    unittest.main()
