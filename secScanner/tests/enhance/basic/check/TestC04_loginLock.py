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
from secScanner.lib.textInfo_basic import *


class TestC04_loginLock(unittest.TestCase):

    @patch("secScanner.enhance.basic.check.C04_loginLock.InsertSection")
    @patch("secScanner.enhance.basic.check.C04_loginLock.get_value")
    @patch("secScanner.enhance.basic.check.C04_loginLock.open", new_callable=mock_open, read_data="auth required pam_faillock.so deny=3\nauth required pam_env.so")
    @patch("secScanner.enhance.basic.check.C04_loginLock.logger")
    @patch("secScanner.enhance.basic.check.C04_loginLock.Display")
    def test_el67_check_deny_correct_setting(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        mock_get_value.side_effect = ["centos", "7"]
        secScanner.enhance.basic.check.C04_loginLock.C04_loginLock()
        mock_logger.info.assert_any_call("Has user login lock Deny set, checking OK")
        mock_display.assert_any_call("- Has user login lock Deny set...", "OK")
   

    @patch("secScanner.enhance.basic.check.C04_loginLock.InsertSection")
    @patch("secScanner.enhance.basic.check.C04_loginLock.get_value")
    @patch("secScanner.enhance.basic.check.C04_loginLock.open", new_callable=mock_open)
    @patch("secScanner.enhance.basic.check.C04_loginLock.logger")
    @patch("secScanner.enhance.basic.check.C04_loginLock.Display")
    def test_oe_el8_check_deny_correct_setting(self, mock_display, mock_logger, mock_open_instance, mock_get_value, mock_insert):
        # Set up two different file reads for the two different files
        mock_open_instance.side_effect = [
            mock_open(read_data="auth required pam_faillock.so deny=6\nauth required pam_env.so").return_value,
            mock_open(read_data="auth required pam_faillock.so deny=4\nauth required pam_env.so").return_value
        ]
        mock_get_value.side_effect = ["rhel", "8"]
        secScanner.enhance.basic.check.C04_loginLock.C04_loginLock()
        mock_logger.info.assert_any_call("Has user login lock Deny set, checking OK")
        mock_display.assert_any_call("- Has user login lock Deny set...", "OK")
    
    @patch("secScanner.enhance.basic.check.C04_loginLock.InsertSection")
    @patch("secScanner.enhance.basic.check.C04_loginLock.get_value")
    @patch("secScanner.enhance.basic.check.C04_loginLock.open", new_callable=mock_open)
    @patch("secScanner.enhance.basic.check.C04_loginLock.logger")
    @patch("secScanner.enhance.basic.check.C04_loginLock.Display")
    def test_oe_el8_check_deny_incorrect_setting(self, mock_display, mock_logger, mock_open_instance, mock_get_value, mock_insert):
        # Set up two different file reads for the two different files
        mock_open_instance.side_effect = [
            mock_open(read_data="auth required pam_faillock.so deny=6\nauth required pam_env.so").return_value,
            mock_open(read_data="auth required pam_faillock.so deny=6\nauth required pam_env.so").return_value,
            mock_open().return_value
        ]
        mock_get_value.side_effect = ["rhel", "8"]
        secScanner.enhance.basic.check.C04_loginLock.C04_loginLock()
        mock_logger.warning.assert_any_call("WRN_C04_01: %s", WRN_C04_01)
        mock_logger.warning.assert_any_call("SUG_C04: %s", SUG_C04)
        mock_display.assert_any_call("- Wrong user login lock Deny set...", "WARNING")

    @patch("secScanner.enhance.basic.check.C04_loginLock.InsertSection")
    @patch("secScanner.enhance.basic.check.C04_loginLock.get_value")
    @patch("secScanner.enhance.basic.check.C04_loginLock.open", new_callable=mock_open, read_data="")
    @patch("secScanner.enhance.basic.check.C04_loginLock.logger")
    @patch("secScanner.enhance.basic.check.C04_loginLock.Display")
    def test_unsupported_os(self, mock_display, mock_logger, mock_file, mock_get_value, mock_insert):
        mock_get_value.side_effect = ["unknown_os", "unknown_version"]
        secScanner.enhance.basic.check.C04_loginLock.C04_loginLock()
        mock_logger.warning.assert_any_call("We do not support unknown_os-unknown_version at this moment")
        mock_display.assert_any_call("- We do not support unknown_os-unknown_version at this moment...", "WARNING")


if __name__ == '__main__':
    unittest.main()

