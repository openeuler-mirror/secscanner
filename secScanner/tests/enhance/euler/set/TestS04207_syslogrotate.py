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
from secScanner.enhance.euler.set.S04207_syslogrotate import S04207_syslogrotate  # Mock test setup.

CONFIG_FILE = '/etc/logrotate.d/rsyslog'
LOG_PATHS = ["/var/log/cron", "/var/log/maillog", "/var/log/messages", "/var/log/secure", "/var/log/spooler"]
FULL_CONFIG = '\n'.join(LOG_PATHS) + '\n{\n    maxage 365\n    rotate 30\n    compress\n    size +4096k\n}\n'
INCOMPLETE_CONFIG = '/var/log/cron\n'

def _open_handle(data=''):
    return mock_open(read_data=data).return_value

class TestS04207_syslogrotate(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.logger')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04207_syslogrotate()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_syslogrotate')
        mock_InsertSection.assert_called_once_with("Set the rsyslog log rotate in /etc/logrotate.d/rsyslog...")
        mock_Display.assert_called_once_with("- Skip set the rsyslog log rotate due to config file...", "SKIPPING")
        mock_add_bak_file.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.logger')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle(INCOMPLETE_CONFIG), _open_handle(), _open_handle(FULL_CONFIG)])
    def test_config_enabled_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S04207_syslogrotate()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_syslogrotate')
        mock_InsertSection.assert_called_once_with("Set the rsyslog log rotate in /etc/logrotate.d/rsyslog...")
        mock_add_bak_file.assert_called_once_with(f'{CONFIG_FILE}_bak')
        mock_Display.assert_called_once_with("- Set the rsyslog log rotate...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.InsertSection')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.Display')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.logger')
    @patch('secScanner.enhance.euler.set.S04207_syslogrotate.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle(INCOMPLETE_CONFIG), _open_handle(), _open_handle(INCOMPLETE_CONFIG)])
    def test_verify_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S04207_syslogrotate()

        # Mock test setup.
        mock_logger.info.assert_called_once_with("the rsyslog log rotate is not set correctly")
        mock_Display.assert_called_once_with("- Set the rsyslog log rotate...", "FAILED")

if __name__ == '__main__':
    unittest.main()
