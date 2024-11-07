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
from unittest.mock import patch, mock_open, MagicMock
from secScanner.lib.textInfo_basic import *
from secScanner.enhance.basic.check.C02_passRemember import C02_passRemember

class TestC02_passRemember(unittest.TestCase):
    @patch('secScanner.enhance.basic.check.C02_passRemember.InsertSection')
    @patch('secScanner.enhance.basic.check.C02_passRemember.open', new_callable=mock_open, read_data='password required pam_unix.so\n')
    @patch('secScanner.enhance.basic.check.C02_passRemember.logger')
    @patch('secScanner.enhance.basic.check.C02_passRemember.Display')
    def test_no_remember_set(self, mock_display, mock_logger, mock_file, mock_insert):
        C02_passRemember()
        mock_logger.warning.assert_any_call("WRN_C02_01: %s", WRN_C02_01)
        mock_logger.warning.assert_any_call("SUG_C02: %s", SUG_C02)
        mock_display.assert_called_with("- No Password Remember set...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C02_passRemember.InsertSection')
    @patch('secScanner.enhance.basic.check.C02_passRemember.open', new_callable=mock_open, read_data='password required pam_unix.so remember=2\n')
    @patch('secScanner.enhance.basic.check.C02_passRemember.logger')
    @patch('secScanner.enhance.basic.check.C02_passRemember.Display')
    def test_remember_set_too_low(self, mock_display, mock_logger, mock_file, mock_insert):
        C02_passRemember()
        mock_logger.warning.assert_any_call("WRN_C02_02: %s", WRN_C02_02)
        mock_logger.warning.assert_any_call("SUG_C02: %s", SUG_C02)
        mock_display.assert_called_with("- Password Remember times is not right...", "WARNING")
    
    @patch('secScanner.enhance.basic.check.C02_passRemember.InsertSection')
    @patch('secScanner.enhance.basic.check.C02_passRemember.open', new_callable=mock_open, read_data='password required pam_unix.so remember=5\n')
    @patch('secScanner.enhance.basic.check.C02_passRemember.logger')
    @patch('secScanner.enhance.basic.check.C02_passRemember.Display')
    def test_remember_set_high(self, mock_display, mock_logger, mock_file, mock_insert):
        C02_passRemember()
        mock_logger.info.assert_called_with("has passwd Remember times set, checking ok")
        mock_display.assert_called_with("- Has Password Remember set...", "OK")

    @patch('secScanner.enhance.basic.check.C02_passRemember.InsertSection')
    @patch('secScanner.enhance.basic.check.C02_passRemember.open', new_callable=mock_open, read_data='password required pam_unix.so remember=#@$**\n')
    @patch('secScanner.enhance.basic.check.C02_passRemember.logger')
    @patch('secScanner.enhance.basic.check.C02_passRemember.Display')
    def test_remember_set_invalid(self, mock_display, mock_logger, mock_file, mock_insert):
        C02_passRemember()
        mock_display.assert_called_with("- Password Remember times is invalid...", "WARNING")

if __name__ == '__main__':
    unittest.main()