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
from secScanner.lib.textInfo_euler import *
from secScanner.enhance.euler.check.C0242_activeHaveged import C0242_activeHaveged
import secScanner

class TestC0242_activeHaveged(unittest.TestCase):
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.InsertSection')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.logger')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_fail_obtain_installation_status(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_getstatusoutput.return_value = (1, '')
        secScanner.enhance.euler.check.C0242_activeHaveged.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0242_activeHaveged()
        mock_InsertSection.assert_any_call("Check if the haveged service is running")
        mock_logger.warning.assert_any_call("WRN_C0242_04: %s", WRN_C0242_04)
        mock_logger.warning.assert_any_call("SUG_C0242_02: %s", SUG_C0242_02)
        mock_display.assert_any_call("- Failed to obtain the installation status of haveged...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.InsertSection')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.logger')
    @patch('secScanner.enhance.euler.check.C0242_activeHaveged.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_haveged_not_installed(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_getstatusoutput.return_value = (0, '')
        secScanner.enhance.euler.check.C0242_activeHaveged.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0242_activeHaveged()
        mock_InsertSection.assert_any_call("Check if the haveged service is running")
        mock_logger.warning.assert_any_call("WRN_C0242_03: %s", WRN_C0242_03)
        mock_logger.warning.assert_any_call("SUG_C0242_02: %s", SUG_C0242_02)
        mock_display.assert_any_call("- Haveged not installed...", "WARNING")
        mock_open.assert_any_call("result_file_path", "a")

if __name__ == '__main__':
    unittest.main()