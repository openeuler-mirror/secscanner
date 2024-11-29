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
from secScanner.enhance.euler.check.C0323_usePAM import C0323_usePAM
import secScanner


class TestC0323_usePAM(unittest.TestCase):

    @patch('secScanner.enhance.euler.check.C0323_usePAM.InsertSection')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.logger')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.Display')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    def test_file_not_exists(self, mock_exists, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟文件不存在
        mock_exists.return_value = False
        config_file = "/etc/ssh/sshd_config"
        secScanner.enhance.euler.check.C0323_usePAM.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        C0323_usePAM()
        mock_InsertSection.assert_any_call("Check set of PAM in sshd config file")
        mock_logger.warning.assert_any_call(f"WRN_C0323: {config_file} {WRN_no_file}")
        mock_logger.warning.assert_any_call(f"SUG_C0323: {config_file} {SUG_no_file}")
        mock_display.assert_any_call(f"- Config file: {config_file} not found...", "SKIPPING")
        mock_open.assert_called_with("result_file_path", "a")
    
    @patch('secScanner.enhance.euler.check.C0323_usePAM.InsertSection')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.logger')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.Display')
    @patch('builtins.open', new_callable=mock_open, read_data = "UsePAM yes\n")
    @patch('os.path.exists')
    def test_correct_config(self, mock_exists, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟文件存在
        mock_exists.return_value = True
        C0323_usePAM()
        mock_InsertSection.assert_any_call("Check set of PAM in sshd config file")
        mock_logger.info.assert_any_call("Check set of PAM in sshd config file")
        mock_display.assert_any_call("- Check set of PAM in sshd config file", "OK")
    
    @patch('secScanner.enhance.euler.check.C0323_usePAM.InsertSection')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.logger')
    @patch('secScanner.enhance.euler.check.C0323_usePAM.Display')
    @patch('builtins.open', new_callable=mock_open, read_data = "UsePAM no\n")
    @patch('os.path.exists')
    def test_incorrect_config(self, mock_exists, mock_open, mock_display, mock_logger, mock_InsertSection):
        # 模拟文件存在
        mock_exists.return_value = True
        secScanner.enhance.euler.check.C0323_usePAM.RESULT_FILE = "result_file_path"  # 假设的结果文件路径
        C0323_usePAM()
        mock_InsertSection.assert_any_call("Check set of PAM in sshd config file")
        mock_logger.warning.assert_any_call("WRN_C0323: %s", WRN_C0323)
        mock_logger.warning.assert_any_call("SUG_C0323: %s", SUG_C0323)
        mock_display.assert_any_call("- Wrong set of PAM in sshd config file...", "WARNING")
        mock_open.assert_called_with("result_file_path", "a")
    
if __name__ == '__main__':
    unittest.main()