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
from secScanner.lib.textInfo_group import *


class TestC001_loginLock(unittest.TestCase):

    @patch("secScanner.enhance.group.check.C001_loginLock.InsertSection")
    @patch("secScanner.enhance.group.check.C001_loginLock.get_value")
    @patch("secScanner.enhance.group.check.C001_loginLock.open", new_callable=mock_open, read_data="auth required pam_faillock.so deny=3\nauth required pam_env.so")
    @patch("secScanner.enhance.group.check.C001_loginLock.logger")
    @patch("secScanner.enhance.group.check.C001_loginLock.Display")
    def test_el7_check_deny_correct_setting(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        mock_get_value.side_effect = ["bclinux", "7"]
        secScanner.enhance.group.check.C001_loginLock.C001_loginLock()
        mock_logger.info.assert_any_call("Has user login lock Deny set, checking OK")
        mock_display.assert_any_call("- Has user login lock Deny set...", "OK")
   
    @patch("secScanner.enhance.group.check.C001_loginLock.InsertSection")
    @patch("secScanner.enhance.group.check.C001_loginLock.get_value")
    @patch("secScanner.enhance.group.check.C001_loginLock.open", new_callable=mock_open, read_data="")
    @patch("secScanner.enhance.group.check.C001_loginLock.logger")
    @patch("secScanner.enhance.group.check.C001_loginLock.Display")
    def test_unsupported_os(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        mock_get_value.side_effect = ["unknown_os", "unknown_version"]
        secScanner.enhance.group.check.C001_loginLock.C001_loginLock()
        mock_logger.warning.assert_any_call("We do not support unknown_os-unknown_version at this moment")
        mock_display.assert_any_call("- We do not support unknown_os-unknown_version at this moment...", "WARNING")

if __name__ == '__main__':
    unittest.main()

