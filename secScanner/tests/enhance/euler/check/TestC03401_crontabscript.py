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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C03401_crontabscript import C03401_crontabscript  # Mock test setup.

CRONTAB_FILE = "/etc/crontab"
SECTION = "Check whether the crontab scripts are only writable by owner"

class TestC03401_crontabscript(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="* * * * * root /usr/local/bin/backup.sh\n")
    def test_script_writable_by_group_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection,
                                              mock_exists, mock_isfile, mock_stat):
        # Mock test setup.
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o777)

        # Mock test setup.
        secScanner.enhance.euler.check.C03401_crontabscript.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_isfile.assert_called_once_with('/usr/local/bin/backup.sh')
        mock_stat.assert_called_once_with('/usr/local/bin/backup.sh')
        mock_file.assert_any_call("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC03401\n")
        mock_logger.warning.assert_any_call("WRN_C03401: %s", WRN_C03401)
        mock_logger.warning.assert_any_call("SUG_C03401: %s", SUG_C03401)
        mock_Display.assert_called_once_with("- Found crontab scripts writable by group or other...", "WARNING")

    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.logger')
    @patch('builtins.open', new_callable=mock_open, read_data="* * * * * root /usr/local/bin/backup.sh\n")
    def test_script_owner_only_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection,
                                  mock_exists, mock_isfile, mock_stat):
        # Mock test setup.
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o755)

        # Mock test setup.
        C03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_file().write.assert_not_called()
        mock_logger.info.assert_called_once_with("Crontab scripts are only writable by owner")
        mock_Display.assert_called_once_with("- Check whether the crontab scripts are only writable by owner...", "OK")

    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.logger')
    @patch('builtins.open', new_callable=mock_open,
           read_data="\n# comment line\n* * * * * root relative.sh\n0 1 * * * root /usr/local/bin/safe.sh\n")
    def test_skip_blank_comment_and_invalid_lines_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection,
                                                     mock_exists, mock_isfile, mock_stat):
        """边界：空行、注释行、字段不足、相对路径命令均应被跳过，仅校验绝对路径脚本"""
        # Mock test setup.
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_stat.return_value = Mock(st_mode=0o755)

        # Mock test setup.
        C03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_isfile.assert_called_once_with('/usr/local/bin/safe.sh')
        mock_stat.assert_called_once_with('/usr/local/bin/safe.sh')
        mock_Display.assert_called_once_with("- Check whether the crontab scripts are only writable by owner...", "OK")

    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.stat')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.isfile')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.os.path.exists')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.InsertSection')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.Display')
    @patch('secScanner.enhance.euler.check.C03401_crontabscript.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found_skipping(self, mock_file, mock_logger, mock_Display, mock_InsertSection,
                                            mock_exists, mock_isfile, mock_stat):
        # Mock test setup.
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C03401_crontabscript.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C03401_crontabscript()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with(SECTION)
        mock_isfile.assert_not_called()
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_logger.warning.assert_any_call(f"WRN_C03401: {CRONTAB_FILE} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C03401: {CRONTAB_FILE} {SUG_no_file}")
        mock_Display.assert_called_once_with(f"- Config file: {CRONTAB_FILE} not found...", "SKIPPING")

if __name__ == '__main__':
    unittest.main()
