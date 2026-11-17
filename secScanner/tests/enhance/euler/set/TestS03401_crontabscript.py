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
from unittest.mock import patch, mock_open, Mock
import logging
from secScanner.enhance.euler.set.S03401_crontabscript import S03401_crontabscript  # Mock test setup.

CRONTAB_FILE = "/etc/crontab"
SCRIPT = "/usr/local/bin/backup.sh"
SECTION = "Set the crontab scripts only writable by owner..."

class TestS03401_crontabscript(unittest.TestCase):

    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.logger')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_disabled_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                      mock_InsertSection, mock_exists):
        # Mock test setup.
        mock_seconf_get.return_value = 'no'

        # Mock test setup.
        S03401_crontabscript()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_crontabscript')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_exists.assert_not_called()
        mock_file.assert_not_called()
        mock_Display.assert_called_once_with("- Skip set the crontab scripts writable permission due to config file...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.logger')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="* * * * * root /usr/local/bin/backup.sh\n")
    def test_chmod_fixed_finished(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                                  mock_exists, mock_isfile, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o666)

        # Mock test setup.
        S03401_crontabscript()

        # Mock test setup.
        mock_seconf_get.assert_called_once_with('euler', 'set_crontabscript')
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_isfile.assert_called_once_with(SCRIPT)
        mock_chmod.assert_called_once_with(SCRIPT, 0o644)
        mock_logger.info.assert_called_once_with("Set crontab scripts only writable by owner finish")
        mock_Display.assert_called_once_with("- Set the crontab scripts only writable by owner...", "FINISHED")

    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.logger')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.seconf.get')
    @patch('builtins.open', new_callable=mock_open, read_data="* * * * * root /usr/local/bin/backup.sh\n")
    def test_chmod_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display, mock_InsertSection,
                          mock_exists, mock_isfile, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o777)
        mock_chmod.side_effect = OSError("operation not permitted")

        # Mock test setup.
        S03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_chmod.assert_called_once_with(SCRIPT, 0o755)
        mock_logger.warning.assert_called_once_with("Set crontab scripts writable permission failed")
        mock_Display.assert_called_once_with("- Set the crontab scripts only writable by owner...", "FAILED")

    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.logger')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.seconf.get')
    @patch('builtins.open', new_callable=mock_open,
           read_data="# comment\n* * * * * root relative.sh\n0 1 * * * root /usr/local/bin/safe.sh\n")
    def test_no_script_needs_fix_skipping(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                          mock_InsertSection, mock_exists, mock_isfile, mock_stat, mock_chmod):
        """边界：注释行、相对路径命令应被跳过；仅属主可写的脚本无需修改，应 SKIPPING"""
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o755)

        # Mock test setup.
        S03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_isfile.assert_called_once_with('/usr/local/bin/safe.sh')
        mock_chmod.assert_not_called()
        mock_logger.info.assert_called_once_with("Crontab scripts already only writable by owner")
        mock_Display.assert_called_once_with("- Crontab scripts already only writable by owner...", "SKIPPING")

    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.chmod')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.logger')
    @patch('secScanner.enhance.euler.set.S03401_crontabscript.seconf.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_failed(self, mock_file, mock_seconf_get, mock_logger, mock_Display,
                                          mock_InsertSection, mock_exists, mock_isfile, mock_stat, mock_chmod):
        # Mock test setup.
        mock_seconf_get.return_value = 'yes'
        mock_exists.return_value = False

        # Mock test setup.
        S03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file.assert_not_called()
        mock_isfile.assert_not_called()
        mock_chmod.assert_not_called()
        mock_logger.warning.assert_called_once_with("crontab config file not exist")
        mock_Display.assert_called_once_with("- crontab config file not exist...", "FAILED")

if __name__ == '__main__':
    unittest.main()
