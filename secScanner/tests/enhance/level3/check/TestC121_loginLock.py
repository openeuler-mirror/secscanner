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
from secScanner.lib.textInfo_level3 import *


class TestC121_loginLock(unittest.TestCase):

    @patch("secScanner.enhance.level3.check.C121_loginLock.InsertSection")
    @patch("secScanner.enhance.level3.check.C121_loginLock.get_value")
    @patch("secScanner.enhance.level3.check.C121_loginLock.open", new_callable=mock_open, read_data="auth required pam_faillock.so deny=3\nauth required pam_env.so")
    @patch("secScanner.enhance.level3.check.C121_loginLock.logger")
    @patch("secScanner.enhance.level3.check.C121_loginLock.Display")
    def test_el67_check_deny_correct_setting(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        mock_get_value.side_effect = ["centos", "7"]
        secScanner.enhance.level3.check.C121_loginLock.C121_loginLock()
        mock_logger.info.assert_any_call("Has user login lock Deny set, checking OK")
        mock_display.assert_any_call("- Has user login lock Deny set...", "OK")
   

    @patch("secScanner.enhance.level3.check.C121_loginLock.InsertSection")
    @patch("secScanner.enhance.level3.check.C121_loginLock.get_value")
    @patch("secScanner.enhance.level3.check.C121_loginLock.open", new_callable=mock_open)
    @patch("secScanner.enhance.level3.check.C121_loginLock.logger")
    @patch("secScanner.enhance.level3.check.C121_loginLock.Display")
    def test_oe_el8_check_deny_correct_setting(self, mock_display, mock_logger, mock_open_instance, mock_get_value, mock_insert):
        # Set up two different file reads for the two different files
        mock_open_instance.side_effect = [
            mock_open(read_data="auth required pam_faillock.so deny=6\nauth required pam_env.so").return_value,
            mock_open(read_data="auth required pam_faillock.so deny=4\nauth required pam_env.so").return_value
        ]
        mock_get_value.side_effect = ["rhel", "8"]
        secScanner.enhance.level3.check.C121_loginLock.C121_loginLock()
        mock_logger.info.assert_any_call("Has user login lock Deny set, checking OK")
        mock_display.assert_any_call("- Has user login lock Deny set...", "OK")

if __name__ == '__main__':
    unittest.main()

