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
from secScanner.enhance.euler.set.S04202_authlog import S04202_authlog  # Mock test setup.

CONFIG_FILE = '/etc/rsyslog.conf'
BAK_FILE = f'{CONFIG_FILE}_bak'
SECTION = "Set the auth events log in /etc/rsyslog.conf..."
AUTH_LINE = 'authpriv.*                                         /var/log/secure\n'
INFO_LINE = '*.info;mail.none;cron.none                         /var/log/messages\n'

def _open_handle(data=''):
    return mock_open(read_data=data).return_value

class TestS04202_authlog(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    def test_config_disabled_skipping(self, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_authlog')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("- Skip set the auth events log due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04202_authlog.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle(INFO_LINE), _open_handle(), _open_handle(INFO_LINE + AUTH_LINE)])
    def test_set_auth_log_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists, mock_copy2):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_authlog')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_copy2.assert_called_once_with(CONFIG_FILE, BAK_FILE)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_getstatusoutput.assert_called_once_with('systemctl restart rsyslog.service')
        mock_file.assert_any_call(CONFIG_FILE, 'a')
        mock_Display.assert_called_once_with("- Set the auth events log...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle(INFO_LINE), _open_handle()])
    def test_restart_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (1, 'restart failed')

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_logger.error.assert_called_once_with('Failed to restart the rsyslog :restart failed')
        mock_Display.assert_called_once_with("- Set the auth events log...", "FAILED")

    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    @patch('builtins.open', side_effect=[_open_handle(INFO_LINE), _open_handle(), _open_handle(INFO_LINE)])
    def test_verify_not_set_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        """边界：配置写入并重启成功，但回读仍无 auth 配置，应 FAILED"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_getstatusoutput.return_value = (0, '')

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_getstatusoutput.assert_called_once_with('systemctl restart rsyslog.service')
        mock_logger.info.assert_any_call("the auth events log is not set correctly")
        mock_Display.assert_called_once_with("- Set the auth events log...", "FAILED")

    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data=INFO_LINE + AUTH_LINE)
    def test_auth_log_already_configured_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_add_bak_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_file.assert_called_once_with(CONFIG_FILE, 'r')
        mock_Display.assert_called_once_with("- Set the auth events log...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S04202_authlog.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04202_authlog.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04202_authlog.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04202_authlog.InsertSection')
    @patch('secScanner.enhance.euler.set.S04202_authlog.Display')
    @patch('secScanner.enhance.euler.set.S04202_authlog.logger')
    @patch('secScanner.enhance.euler.set.S04202_authlog.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection, mock_add_bak_file, mock_getstatusoutput, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S04202_authlog()

        # Mock test setup.
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with(f"- {CONFIG_FILE} does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
