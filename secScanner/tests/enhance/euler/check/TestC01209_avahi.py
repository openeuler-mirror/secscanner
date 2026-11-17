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
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C01209_avahi import C01209_avahi  # Mock test setup.

class TestC01209_avahi(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.check.C01209_avahi.Display')
    @patch('secScanner.enhance.euler.check.C01209_avahi.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_avahi_installed_warning(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (0, 'avahi-0.8-13.oe1.x86_64')

        # Mock test setup.
        secScanner.enhance.euler.check.C01209_avahi.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the avahi software is installed in your Linux System")
        mock_getstatusoutput.assert_called_once_with('rpm -q avahi')
        mock_file.assert_called_once_with("check_result.relt", "a", encoding="utf-8")
        mock_file().write.assert_called_once_with("\nC01209\n")
        mock_logger.warning.assert_any_call("WRN_C01209: %s", WRN_C01209)
        mock_logger.warning.assert_any_call("SUG_C01209: %s", SUG_C01209)
        mock_Display.assert_called_once_with("- Check the avahi software is installed...", "WARNING")

    @patch('secScanner.enhance.euler.check.C01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.check.C01209_avahi.Display')
    @patch('secScanner.enhance.euler.check.C01209_avahi.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_avahi_not_installed_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        # Mock test setup.
        mock_getstatusoutput.return_value = (1, 'package avahi is not installed')

        # Mock test setup.
        secScanner.enhance.euler.check.C01209_avahi.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the avahi software is installed in your Linux System")
        mock_getstatusoutput.assert_called_once_with('rpm -q avahi')
        mock_file.assert_not_called()
        mock_logger.warning.assert_not_called()
        mock_logger.info.assert_called_once_with("The avahi status is: package avahi is not installed")
        mock_Display.assert_called_once_with("- Check the avahi software is uninstall...", "OK")

    @patch('secScanner.enhance.euler.check.C01209_avahi.subprocess.getstatusoutput')
    @patch('secScanner.enhance.euler.check.C01209_avahi.InsertSection')
    @patch('secScanner.enhance.euler.check.C01209_avahi.Display')
    @patch('secScanner.enhance.euler.check.C01209_avahi.logger')
    @patch('builtins.open', new_callable=mock_open)
    def test_rpm_command_not_found_ok(self, mock_file, mock_logger, mock_Display, mock_InsertSection, mock_getstatusoutput):
        """边界：rpm 命令不可用（返回码 127、输出为空）应视为未安装，输出 OK"""
        # Mock test setup.
        mock_getstatusoutput.return_value = (127, '')

        # Mock test setup.
        secScanner.enhance.euler.check.C01209_avahi.RESULT_FILE = "check_result.relt"

        # Mock test setup.
        C01209_avahi()

        # Mock test setup.
        mock_InsertSection.assert_called_once_with("Check whether the avahi software is installed in your Linux System")
        mock_file.assert_not_called()
        mock_logger.info.assert_called_once_with("The avahi status is: ")
        mock_Display.assert_called_once_with("- Check the avahi software is uninstall...", "OK")

if __name__ == '__main__':
    unittest.main()
