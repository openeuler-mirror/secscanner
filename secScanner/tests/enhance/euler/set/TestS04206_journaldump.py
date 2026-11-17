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
from secScanner.enhance.euler.set.S04206_journaldump import S04206_journaldump  # Mock test setup.

CONFIG_FILE = '/etc/rsyslog.conf'
JOURNAL_LINE = 'module(load="imjournal")\n'

def _open_handle(data=''):
    return mock_open(read_data=data).return_value

class TestS04206_journaldump(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04206_journaldump.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.Display')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.logger')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04206_journaldump()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_journaldump')
        mock_InsertSection.assert_called_once_with("Set the rsyslog dump journald log in /etc/rsyslog.conf...")
        mock_Display.assert_called_once_with("- Skip set the rsyslog dump journald log due to config file...", "SKIPPING")
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04206_journaldump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.Display')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.logger')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle('*.info\n'), _open_handle(), _open_handle(JOURNAL_LINE)])
    def test_config_enabled_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S04206_journaldump()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_journaldump')
        mock_InsertSection.assert_called_once_with("Set the rsyslog dump journald log in /etc/rsyslog.conf...")
        mock_add_bak_file.assert_called_once_with(f'{CONFIG_FILE}_bak')
        mock_getstatusoutput.assert_called_once_with('systemctl restart rsyslog.service')
        mock_Display.assert_called_once_with("- Set the rsyslog dump journald log...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S04206_journaldump.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.InsertSection')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.Display')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.logger')
    @patch('secScanner.enhance.euler.set.S04206_journaldump.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle('*.info\n'), _open_handle()])
    def test_restart_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (1, 'restart failed')

        # Mock test setup.
        S04206_journaldump()

        # Mock test setup.
        mock_logger.error.assert_called_once_with('Failed to restart the rsyslog :restart failed')
        mock_Display.assert_called_once_with("- Set the rsyslog dump journald log...", "FAILED")

if __name__ == '__main__':
    unittest.main()
