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
import os
import sys
import secScanner
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0364_sysrq import C0364_sysrq

class TestC0364_sysrq(unittest.TestCase):
    @patch('secScanner.enhance.euler.check.C0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.logger')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.Display')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=0\n")
    def test_sysrq_correct_setting(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        mock_exists.return_value = True
        
        C0364_sysrq()
        
        mock_InsertSection.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_Display.assert_called_once_with("- Check set of kernel.sysrq in sysctl config file", "OK")
        mock_logger.info.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_file.assert_called_with("/etc/sysctl.conf", "r")
    
    @patch('secScanner.enhance.euler.check.C0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.logger')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.Display')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=1\n")
    def test_sysrq_incorrect_setting(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0364_sysrq.RESULT_FILE = "result_file_path"
        
        C0364_sysrq()
        
        mock_InsertSection.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_Display.assert_called_once_with("- Wrong set of kernel.sysrq in sysctl config file...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0364: %s", WRN_C0364)
        mock_logger.warning.assert_any_call("SUG_C0364: %s", SUG_C0364)
        mock_file.assert_any_call("/etc/sysctl.conf", "r")
        mock_file.assert_any_call("result_file_path", "a")
    
    @patch('secScanner.enhance.euler.check.C0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.logger')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.Display')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open)
    def test_sysrq_file_not_exists(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        mock_exists.return_value = False
        secScanner.enhance.euler.check.C0364_sysrq.RESULT_FILE = "result_file_path"
        
        C0364_sysrq()
        
        mock_InsertSection.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_Display.assert_called_once_with("- Config file: /etc/sysctl.conf not found...", "SKIPPING")
        mock_logger.warning.assert_any_call(f"WRN_C0364: /etc/sysctl.conf {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0364: /etc/sysctl.conf {SUG_no_file}")
        mock_file.assert_called_once_with("result_file_path", "a")

    @patch('secScanner.enhance.euler.check.C0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.logger')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.Display')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=0\nsome other config\nkernel.sysrq=0\n")
    def test_sysrq_multiple_settings(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0364_sysrq.RESULT_FILE = "result_file_path"
        
        C0364_sysrq()
        
        mock_InsertSection.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_Display.assert_called_once_with("- Wrong set of kernel.sysrq in sysctl config file...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0364: %s", WRN_C0364)
        mock_logger.warning.assert_any_call("SUG_C0364: %s", SUG_C0364)
        mock_file.assert_any_call("/etc/sysctl.conf", "r")
        mock_file.assert_any_call("result_file_path", "a")

    @patch('secScanner.enhance.euler.check.C0364_sysrq.os.path.exists')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.logger')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.Display')
    @patch('secScanner.enhance.euler.check.C0364_sysrq.InsertSection')
    @patch('builtins.open', new_callable=mock_open, read_data="kernel.sysrq=0\nsome other config\nkernel.sysrq=1\n")
    def test_sysrq_conflicting_settings(self, mock_file, mock_InsertSection, mock_Display, mock_logger, mock_exists):
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0364_sysrq.RESULT_FILE = "result_file_path"
        
        C0364_sysrq()
        
        mock_InsertSection.assert_called_once_with("Check set of kernel.sysrq in sysctl config file")
        mock_Display.assert_called_once_with("- Wrong set of kernel.sysrq in sysctl config file...", "WARNING")
        mock_logger.warning.assert_any_call("WRN_C0364: %s", WRN_C0364)
        mock_logger.warning.assert_any_call("SUG_C0364: %s", SUG_C0364)
        mock_file.assert_any_call("/etc/sysctl.conf", "r")
        mock_file.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()
