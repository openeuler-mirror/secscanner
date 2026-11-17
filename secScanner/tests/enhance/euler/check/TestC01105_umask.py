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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01105_umask import C01105_umask  # Mock test setup.

class TestC01105_umask(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01105_umask.seconf.get')
    @patch('secScanner.enhance.euler.check.C01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.check.C01105_umask.Display')
    @patch('secScanner.enhance.euler.check.C01105_umask.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_wrong_umask_value(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_seconf_get):
        # Mock test setup.
        mock_seconf_get.return_value = '027'
        mock_exists.return_value = True
        mock_file.return_value.readlines.return_value = ['umask 022\n']

        # Mock test setup.
        secScanner.enhance.euler.check.C01105_umask.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01105_umask()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the UMASK config is right")
        mock_seconf_get.assert_called_once_with('euler', 'umask_value')
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01105\n")
        mock_logger.warning.assert_any_call("WRN_C01105: %s", WRN_C01105)
        mock_logger.warning.assert_any_call("SUG_C01105: %s", SUG_C01105)
        mock_Display.assert_any_call("- Check wrong set of UMASK...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01105_umask.seconf.get')
    @patch('secScanner.enhance.euler.check.C01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.check.C01105_umask.Display')
    @patch('secScanner.enhance.euler.check.C01105_umask.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_correct_umask_value(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_seconf_get):
        # Mock test setup.
        mock_seconf_get.return_value = '027'
        mock_exists.return_value = True
        mock_file.return_value.readlines.return_value = ['# umask setting\n', 'umask 027\n']

        # Mock test setup.
        C01105_umask()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the UMASK config is right")
        mock_file().write.assert_not_called()
        mock_logger.info.assert_any_call("The UMASK config is right, checking ok")
        mock_Display.assert_any_call("- Check whether the UMASK config is right...", "OK")

    @patch('secScanner.enhance.euler.check.C01105_umask.seconf.get')
    @patch('secScanner.enhance.euler.check.C01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.check.C01105_umask.Display')
    @patch('secScanner.enhance.euler.check.C01105_umask.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_config_file_not_found(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_seconf_get):
        """边界：配置文件不存在时应记录结果并跳过检查"""
        # Mock test setup.
        mock_seconf_get.return_value = '027'
        mock_exists.return_value = False

        # Mock test setup.
        secScanner.enhance.euler.check.C01105_umask.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01105_umask()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the UMASK config is right")
        mock_file.assert_called_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01105\n")
        mock_logger.warning.assert_any_call("WRN_C01105: %s %s", "/etc/bashrc", WRN_no_file)
        mock_logger.warning.assert_any_call("SUG_C01105: %s %s", "/etc/bashrc", SUG_no_file)
        mock_Display.assert_any_call("- Config file: %s not found..." % "/etc/bashrc", "SKIPPING")

    @patch('secScanner.enhance.euler.check.C01105_umask.seconf.get')
    @patch('secScanner.enhance.euler.check.C01105_umask.os.path.exists')
    @patch('secScanner.enhance.euler.check.C01105_umask.InsertSection')
    @patch('secScanner.enhance.euler.check.C01105_umask.Display')
    @patch('secScanner.enhance.euler.check.C01105_umask.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_non_octal_umask_matched_as_string(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_exists, mock_seconf_get):
        """边界：非八进制形式的 umask 值与配置字符串一致时应判定合规"""
        # Mock test setup.
        mock_seconf_get.return_value = 'u=rwx,g=rx,o='
        mock_exists.return_value = True
        mock_file.return_value.readlines.return_value = ['umask u=rwx,g=rx,o=\n']

        # Mock test setup.
        C01105_umask()

        # Mock test setup.
        mock_file().write.assert_not_called()
        mock_logger.info.assert_any_call("The UMASK config is right, checking ok")
        mock_Display.assert_any_call("- Check whether the UMASK config is right...", "OK")

if __name__ == '__main__':
    unittest.main()
