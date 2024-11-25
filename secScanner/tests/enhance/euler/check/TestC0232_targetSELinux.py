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
from secScanner.enhance.euler.check.C0232_targetSELinux import C0232_targetSELinux
import secScanner

class TestC0232_targetSELinux(unittest.TestCase):

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_policy_correct(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_getstatusoutput.return_value = (0, 'Loaded policy name: targeted')
        # 调用测试函数
        C0232_targetSELinux()
        mock_InsertSection.assert_called_with("check SELinux policy")
        mock_logger.info.assert_any_call("SELinux policy configuration is correct, checking ok")
        mock_display.assert_any_call("- check SELinux policy...", "OK")
    
    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_policy_incorrect(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_getstatusoutput.return_value = (0, 'Loaded policy name: not-targeted')
        secScanner.enhance.euler.check.C0232_targetSELinux.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0232_targetSELinux()
        mock_InsertSection.assert_called_with("check SELinux policy")
        mock_logger.warning.assert_any_call("WRN_C0232_01: %s", WRN_C0232_01)
        mock_logger.warning.assert_any_call("SUG_C0232_01: %s", SUG_C0232_01)
        mock_display.assert_any_call("- Incorrect SELinux policy settings...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")

    @patch('os.path.exists')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.InsertSection')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.logger')
    @patch('secScanner.enhance.euler.check.C0232_targetSELinux.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.getstatusoutput')
    def test_fail_obtain_policy(self, mock_getstatusoutput, mock_open, mock_display, mock_logger, mock_InsertSection, mock_exists):
        mock_getstatusoutput.return_value = (1, '')
        secScanner.enhance.euler.check.C0232_targetSELinux.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        # 调用测试函数
        C0232_targetSELinux()
        mock_InsertSection.assert_called_with("check SELinux policy")
        mock_logger.warning.assert_any_call("WRN_C0232_02: %s", WRN_C0232_02)
        mock_logger.warning.assert_any_call("SUG_C0232_02: %s", SUG_C0232_02)
        mock_display.assert_any_call("- Failed to obtain SELinux policy...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
        
if __name__ == '__main__':
    unittest.main()