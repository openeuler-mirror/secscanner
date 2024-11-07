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
from secScanner.lib.textInfo_basic import *
import secScanner

class TestC03_passComplex(unittest.TestCase):
    def setUp(self):
        self.base_data = "password requisite pam_pwquality.so "

    @patch('secScanner.enhance.basic.check.C03_passComplex.InsertSection')
    @patch('secScanner.enhance.basic.check.C03_passComplex.open', new_callable=mock_open)
    @patch('secScanner.enhance.basic.check.C03_passComplex.logger')
    @patch('secScanner.enhance.basic.check.C03_passComplex.Display')
    def test_no_settings(self, mock_display, mock_logger, mock_open, mock_insert):
        mock_open.return_value.readlines.return_value = [self.base_data]
        secScanner.enhance.basic.check.C03_passComplex.C03_passComplex()
        mock_display.assert_any_call("- No Password Minlen set...", "WARNING")
        mock_display.assert_any_call("- No Password Minclass set...", "WARNING")
        mock_display.assert_any_call("- No Password ucredit set...", "WARNING")
        mock_display.assert_any_call("- No Password lcredit set...", "WARNING")
        mock_display.assert_any_call("- No Password dcredit set...", "WARNING")
        mock_display.assert_any_call("- No Password ocredit set...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C03_passComplex.InsertSection')
    @patch('secScanner.enhance.basic.check.C03_passComplex.open', new_callable=mock_open)
    @patch('secScanner.enhance.basic.check.C03_passComplex.logger')
    @patch('secScanner.enhance.basic.check.C03_passComplex.Display')
    def test_incorrect_minlen(self, mock_display, mock_logger, mock_open, mock_insert):
        data = self.base_data + "minlen=5"
        mock_open.return_value.readlines.return_value = [data]
        secScanner.enhance.basic.check.C03_passComplex.C03_passComplex()
        mock_display.assert_any_call("- Wrong Password Minlen set...", "WARNING")
        mock_display.assert_any_call("- No Password Minclass set...", "WARNING")
        mock_display.assert_any_call("- No Password ucredit set...", "WARNING")
        mock_display.assert_any_call("- No Password lcredit set...", "WARNING")
        mock_display.assert_any_call("- No Password dcredit set...", "WARNING")
        mock_display.assert_any_call("- No Password ocredit set...", "WARNING")


if __name__ == '__main__':
    unittest.main()
