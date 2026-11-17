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
from secScanner.enhance.euler.set.S01209_avahi import S01209_avahi  # Mock test setup.

class TestS01209_avahi(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S01209_avahi.os.system')
    @patch('secScanner.enhance.euler.set.S01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.set.S01209_avahi.Display')
    @patch('secScanner.enhance.euler.set.S01209_avahi.logger')
    @patch('secScanner.enhance.euler.set.S01209_avahi.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_system):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S01209_avahi()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_avahi')
        mock_InsertSection.assert_called_once_with("Remove the avahi in your Linux System...")
        mock_getstatusoutput.assert_not_called()
        mock_system.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set remove the avahi...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01209_avahi.os.system')
    @patch('secScanner.enhance.euler.set.S01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.set.S01209_avahi.Display')
    @patch('secScanner.enhance.euler.set.S01209_avahi.logger')
    @patch('secScanner.enhance.euler.set.S01209_avahi.seconf.get')
    def test_not_installed_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_system):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.return_value = (1, 'package avahi is not installed')

        # Mock test setup.
        S01209_avahi()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_avahi')
        mock_InsertSection.assert_called_once_with("Remove the avahi in your Linux System...")
        mock_getstatusoutput.assert_called_once_with('rpm -q avahi')
        mock_system.assert_not_called()
        mock_logger.info.assert_called_once_with('The status is:package avahi is not installed')
        mock_Display.assert_called_once_with("- No package for the avahi...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S01209_avahi.os.system')
    @patch('secScanner.enhance.euler.set.S01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.set.S01209_avahi.Display')
    @patch('secScanner.enhance.euler.set.S01209_avahi.logger')
    @patch('secScanner.enhance.euler.set.S01209_avahi.seconf.get')
    def test_remove_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_system):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'avahi-0.8-13.oe1.x86_64'), (0, 'Removed: avahi')]

        # Mock test setup.
        S01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the avahi in your Linux System...")
        mock_getstatusoutput.assert_any_call('rpm -q avahi')
        mock_getstatusoutput.assert_any_call('yum remove avahi -y')
        mock_system.assert_not_called()
        mock_logger.info.assert_called_once_with("Set remove the avahi, checking ok")
        mock_Display.assert_called_once_with("- Set remove the avahi...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01209_avahi.os.system')
    @patch('secScanner.enhance.euler.set.S01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.set.S01209_avahi.Display')
    @patch('secScanner.enhance.euler.set.S01209_avahi.logger')
    @patch('secScanner.enhance.euler.set.S01209_avahi.seconf.get')
    def test_remove_failed_disable_success_finished(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_system):
        """边界：yum 卸载失败但 systemctl disable 成功，应视为 FINISHED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'avahi-0.8-13.oe1.x86_64'), (1, 'Error: remove failed')]
        mock_system.return_value = 0

        # Mock test setup.
        S01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the avahi in your Linux System...")
        mock_system.assert_called_once_with('systemctl --now disable avahi-daemon')
        mock_logger.info.assert_called_once_with("Failed to remove the avahi, set disabled the avahi-daemon instead")
        mock_Display.assert_called_once_with("- Set disabled the avahi-daemon instead...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S01209_avahi.os.system')
    @patch('secScanner.enhance.euler.set.S01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.set.S01209_avahi.Display')
    @patch('secScanner.enhance.euler.set.S01209_avahi.logger')
    @patch('secScanner.enhance.euler.set.S01209_avahi.seconf.get')
    def test_remove_and_disable_failed(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput, mock_system):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_getstatusoutput.side_effect = [(0, 'avahi-0.8-13.oe1.x86_64'), (1, 'Error: remove failed')]
        mock_system.return_value = 1

        # Mock test setup.
        S01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Remove the avahi in your Linux System...")
        mock_system.assert_called_once_with('systemctl --now disable avahi-daemon')
        mock_logger.warning.assert_called_once_with("Set remove the avahi failed")
        mock_Display.assert_called_once_with("- Set remove the avahi...", "FAILED")

if __name__ == '__main__':
    unittest.main()
