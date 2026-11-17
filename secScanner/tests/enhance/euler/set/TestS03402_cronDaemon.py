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
from unittest.mock import patch, Mock
from secScanner.enhance.euler.set.S03402_cronDaemon import S03402_cronDaemon  # Mock test setup.

class TestS03402_cronDaemon(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.logger')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03402_cronDaemon()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_cronDaemon')
        mock_InsertSection.assert_called_once_with("Set the cron daemon enabled...")
        mock_run.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with("- Skip enable the cron daemon due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.logger')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.seconf.get')
    def test_enable_cron_daemon_finished(self, mock_seconf_get, mock_logger, mock_Display,
                                         mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = Mock(stdout=b'disabled')
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S03402_cronDaemon()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_cronDaemon')
        mock_getstatusoutput.assert_called_once_with('systemctl --now enable crond')
        mock_logger.info.assert_any_call("Enable the cron daemon finish")
        mock_Display.assert_called_once_with("- Enable the cron daemon...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.logger')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.seconf.get')
    def test_enable_cron_daemon_failed(self, mock_seconf_get, mock_logger, mock_Display,
                                       mock_InsertSection, mock_run, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = Mock(stdout=b'disabled')
        mock_getstatusoutput.return_value = (1, 'Failed to enable unit')

        # Mock test setup.
        S03402_cronDaemon()

        # Mock test setup.
        mock_getstatusoutput.assert_called_once_with('systemctl --now enable crond')
        mock_logger.warning.assert_called_once_with("Enable the cron daemon failed")
        mock_Display.assert_called_once_with("- Enable the cron daemon...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.subprocess.run')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.InsertSection')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.Display')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.logger')
    @patch('secScanner.enhance.euler.set.S03402_cronDaemon.seconf.get')
    def test_cron_daemon_already_enabled_boundary(self, mock_seconf_get, mock_logger, mock_Display,
                                                   mock_InsertSection, mock_run, mock_getstatusoutput):
        """边界：crond 已处于 enabled 状态，无需再次启用，应视为 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_run.return_value = Mock(stdout=b'enabled')

        # Mock test setup.
        S03402_cronDaemon()

        # Mock test setup.
        mock_getstatusoutput.assert_not_called()
        mock_logger.info.assert_called_once_with("The cron daemon already enabled")
        mock_Display.assert_called_once_with("- The cron daemon has already been enabled...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
