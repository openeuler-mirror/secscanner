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
from secScanner.enhance.euler.set.S04111_logsizelimit import S04111_logsizelimit  # Mock test setup.

CONFIG_FILE = '/etc/audit/auditd.conf'
BAK_FILE = '/etc/audit/auditd.conf_bak'
SECTION = "Set the audit log size limit in /etc/audit/auditd.conf..."
MAX_LOG_FILE_VALUE = '8'

class TestS04111_logsizelimit(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                                      mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_logsizelimit')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_Display.assert_called_once_with("- Skip set the audit log size limit due to config file...", "SKIPPING")
        mock_exists.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="max_log_file = 8\n")
    def test_logsizelimit_already_set_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                              mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                                              mock_getstatusoutput):
        """边界：max_log_file 已为合法正整数，应直接 SKIPPING 且不重启服务"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_logsizelimit')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_called_once_with(CONFIG_FILE, "r")
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_logger.info.assert_called_once_with("the audit log size limit is already set")
        mock_Display.assert_called_once_with("- Set the audit log size limit...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_logsizelimit_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                                      mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]
        mock_getstatusoutput.return_value = (0, '')
        mock_file().readlines.side_effect = [
            ["max_log_file = 0\n"],
            ["max_log_file = 8\n"],
        ]

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_logsizelimit')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_copy2.assert_not_called()
        mock_getstatusoutput.assert_called_once_with('service auditd restart')
        mock_file().write.assert_any_call(f'max_log_file = {MAX_LOG_FILE_VALUE}\n')
        mock_logger.info.assert_called_once_with("the audit log size limit is set, checking ok")
        mock_Display.assert_called_once_with("- Set the audit log size limit...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_set_logsizelimit_verify_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                           mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                                           mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, False]
        mock_getstatusoutput.return_value = (0, '')
        mock_file().readlines.side_effect = [
            ["max_log_file = 0\n"],
            ["max_log_file = 0\n"],
        ]

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_copy2.assert_called_once_with(CONFIG_FILE, BAK_FILE)
        mock_add_bak_file.assert_called_once_with(BAK_FILE)
        mock_logger.info.assert_called_once_with("the audit log size limit is not set correctly")
        mock_Display.assert_called_once_with("- Set the audit log size limit...", "FAILED")

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_restart_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                            mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                            mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.side_effect = [True, True]
        mock_getstatusoutput.return_value = (1, 'restart failed')
        mock_file().readlines.side_effect = [
            ["max_log_file = 0\n"],
        ]

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_logger.error.assert_called_once_with("Failed to restart the auditd :restart failed")
        mock_Display.assert_called_once_with("- Set the audit log size limit...", "FAILED")

    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.add_bak_file')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.shutil.copy2')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.os.path.exists')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.InsertSection')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.Display')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.logger')
    @patch('secScanner.enhance.euler.set.S04111_logsizelimit.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                           mock_InsertSection, mock_exists, mock_copy2, mock_add_bak_file,
                                           mock_getstatusoutput):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S04111_logsizelimit()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_not_called()
        mock_copy2.assert_not_called()
        mock_add_bak_file.assert_not_called()
        mock_getstatusoutput.assert_not_called()
        mock_Display.assert_called_once_with(f"- {CONFIG_FILE} does not exist...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
